import torch
import numpy as np
import cv2
import os
from PIL import Image
from scipy.ndimage import zoom, gaussian_filter
from scipy.special import logsumexp
import deepgaze_pytorch

class SaliencyModel:
    def __init__(self, enhanced_mode=True):
        """
        Enhanced Saliency Model with UI/UX-specific improvements.
        
        Args:
            enhanced_mode (bool): If True, applies UI-specific enhancements.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.enhanced_mode = enhanced_mode
        
        print(f"Loading DeepGaze IIE Model on {self.device}...")
        print(f"Enhanced Mode: {'ENABLED' if enhanced_mode else 'DISABLED'}")
        
        # Load DeepGaze IIE
        self.model = deepgaze_pytorch.DeepGazeIIE(pretrained=True).to(self.device)
        self.model.eval()
        
        # Load Center Bias
        if os.path.exists("centerbias_mit1003.npy"):
            self.centerbias_template = np.load("centerbias_mit1003.npy")
        else:
            print("Warning: Center bias file not found. Using uniform bias.")
            self.centerbias_template = np.zeros((1024, 1024))
        
        # Load Face Detector (OpenCV Haar Cascade)
        if enhanced_mode:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            print("Face detector loaded.")

    def detect_faces(self, img_np):
        """
        Detect faces in the image and return a face salience map.
        """
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        h, w = img_np.shape[:2]
        face_map = np.zeros((h, w), dtype=np.float32)
        
        for (x, y, fw, fh) in faces:
            # Create elliptical mask for each face
            center = (x + fw//2, y + fh//2)
            axes = (fw//2, fh//2)
            cv2.ellipse(face_map, center, axes, 0, 0, 360, 1.0, -1)
        
        # Smooth the face map
        if face_map.max() > 0:
            face_map = gaussian_filter(face_map, sigma=fw//4 if len(faces) > 0 else 20)
        
        return face_map, len(faces)

    def detect_text_regions(self, img_np):
        """
        Detect likely text regions using edge density and gradients.
        """
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        
        # Text typically has high gradient variance
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
        
        # Normalize
        text_map = (gradient_magnitude - gradient_magnitude.min()) / (gradient_magnitude.max() - gradient_magnitude.min() + 1e-8)
        
        # Apply threshold to focus on high-gradient areas (text)
        text_map = np.where(text_map > 0.3, text_map, 0)
        
        # Smooth
        text_map = gaussian_filter(text_map, sigma=5)
        
        return text_map

    def apply_f_pattern_bias(self, h, w):
        """
        Apply F-Pattern reading bias (common in web pages).
        Higher saliency at top-left, decreasing towards bottom-right.
        """
        y_coords, x_coords = np.ogrid[:h, :w]
        
        # Top-left quadrant gets highest bias
        # Linear decay from top-left to bottom-right
        x_bias = 1.0 - (x_coords / w) * 0.5  # Decay 50% left to right
        y_bias = 1.0 - (y_coords / h) * 0.6  # Decay 60% top to bottom
        
        f_pattern = x_bias * y_bias
        
        # Smooth the bias
        f_pattern = gaussian_filter(f_pattern, sigma=min(h, w) // 10)
        
        return f_pattern

    def predict(self, image_path):
        """
        Predicts saliency map using DeepGaze IIE + UI/UX enhancements.
        """
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_dir, f"saliency_{filename}")

        # Load image
        try:
            pil_img = Image.open(image_path).convert('RGB')
            img_np = np.array(pil_img)
        except Exception as e:
            raise ValueError(f"Could not process image: {e}")

        h, w = img_np.shape[:2]
        
        # === STEP 1: DeepGaze IIE Prediction ===
        centerbias = zoom(self.centerbias_template, (h/self.centerbias_template.shape[0], w/self.centerbias_template.shape[1]), order=0, mode='nearest')
        centerbias -= logsumexp(centerbias)
        
        image_tensor = torch.tensor([img_np.transpose(2, 0, 1)]).to(self.device)
        centerbias_tensor = torch.tensor([centerbias]).to(self.device)

        with torch.no_grad():
            log_density_prediction = self.model(image_tensor, centerbias_tensor)
            density = np.exp(log_density_prediction.cpu().numpy()[0, 0])
        
        # Normalize to [0, 1]
        saliency = (density - density.min()) / (density.max() - density.min() + 1e-8)
        
        # === STEP 2: UI/UX Enhancements ===
        if self.enhanced_mode:
            print("Applying UI/UX enhancements...")
            
            # 1. Face Detection Boost
            face_map, num_faces = self.detect_faces(img_np)
            if num_faces > 0:
                print(f"  - Detected {num_faces} face(s). Boosting face regions.")
                face_map_norm = face_map / (face_map.max() + 1e-8)
                saliency = saliency + face_map_norm * 0.3  # 30% boost for faces
            
            # 2. Text Region Boost
            text_map = self.detect_text_regions(img_np)
            print(f"  - Boosting text regions.")
            saliency = saliency + text_map * 0.15  # 15% boost for text
            
            # 3. F-Pattern Bias (for web/UI layouts)
            f_bias = self.apply_f_pattern_bias(h, w)
            print(f"  - Applying F-pattern reading bias.")
            saliency = saliency * (0.7 + f_bias * 0.3)  # Blend with 30% F-pattern weight
            
            # Re-normalize after enhancements
            saliency = (saliency - saliency.min()) / (saliency.max() - saliency.min() + 1e-8)
        
        # === STEP 3: Visualization ===
        saliency_uint8 = (saliency * 255).astype(np.uint8)
        heatmap = cv2.applyColorMap(saliency_uint8, cv2.COLORMAP_JET)
        
        cv_img = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        result = cv2.addWeighted(cv_img, 0.6, heatmap, 0.4, 0)
        
        cv2.imwrite(output_path, result)
        print(f"Saliency map saved to: {output_path}")
        return output_path
