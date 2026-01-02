import torch
import numpy as np
import cv2
import os
from PIL import Image
from scipy.ndimage import zoom
from scipy.special import logsumexp
import deepgaze_pytorch

class SaliencyModel:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Loading DeepGaze IIE Model on {self.device}...")
        
        # Load DeepGaze IIE
        # This will download weights automatically on first run
        self.model = deepgaze_pytorch.DeepGazeIIE(pretrained=True).to(self.device)
        self.model.eval()
        
        # Load Center Bias
        if os.path.exists("centerbias_mit1003.npy"):
            self.centerbias_template = np.load("centerbias_mit1003.npy")
        else:
            print("Warning: Center bias file not found. Using uniform bias.")
            self.centerbias_template = np.zeros((1024, 1024))

    def predict(self, image_path):
        """
        Predicts saliency map using DeepGaze IIE.
        """
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_dir, f"saliency_{filename}")

        # Load image
        try:
            # DeepGaze expects numpy array (H, W, 3) in RGB
            pil_img = Image.open(image_path).convert('RGB')
            img_np = np.array(pil_img)
        except Exception as e:
            raise ValueError(f"Could not process image: {e}")

        # Prepare Center Bias
        # Rescale to match image size
        h, w = img_np.shape[:2]
        centerbias = zoom(self.centerbias_template, (h/self.centerbias_template.shape[0], w/self.centerbias_template.shape[1]), order=0, mode='nearest')
        # Renormalize log density
        centerbias -= logsumexp(centerbias)
        
        # Prepare Tensors
        # Image: (1, 3, H, W)
        image_tensor = torch.tensor([img_np.transpose(2, 0, 1)]).to(self.device)
        centerbias_tensor = torch.tensor([centerbias]).to(self.device)

        # Inference
        with torch.no_grad():
            # Output is log density
            log_density_prediction = self.model(image_tensor, centerbias_tensor)
            
            # Convert log density to probability distribution
            density = np.exp(log_density_prediction.cpu().numpy()[0, 0])
            
        # Normalize to 0-255 for visualization
        saliency = (density - density.min()) / (density.max() - density.min() + 1e-8)
        saliency = (saliency * 255).astype(np.uint8)
        
        # Apply heatmap
        heatmap = cv2.applyColorMap(saliency, cv2.COLORMAP_JET)
        
        # Overlay
        # Convert RGB to BGR for OpenCV
        cv_img = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        result = cv2.addWeighted(cv_img, 0.6, heatmap, 0.4, 0)
        
        cv2.imwrite(output_path, result)
        return output_path
