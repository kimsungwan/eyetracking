import cv2
import numpy as np
import os
from report_generator import generate_report

def create_dummy_images():
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    
    # Create dummy original image (random noise + some shapes)
    original = np.zeros((800, 600, 3), dtype=np.uint8)
    cv2.circle(original, (300, 400), 100, (0, 0, 255), -1) # Red circle
    cv2.rectangle(original, (100, 100), (200, 200), (0, 255, 0), -1) # Green rect
    cv2.imwrite("uploads/test_image.jpg", original)
    
    # Create dummy saliency map (grayscale)
    saliency = np.zeros((800, 600), dtype=np.uint8)
    cv2.circle(saliency, (300, 400), 100, 255, -1) # High saliency at red circle
    cv2.rectangle(saliency, (100, 100), (200, 200), 128, -1) # Medium saliency
    cv2.imwrite("outputs/saliency_test_image.jpg", saliency)
    
    return "uploads/test_image.jpg", "outputs/saliency_test_image.jpg"

def test_generation():
    print("Starting test_generation...", flush=True)
    print("Creating dummy data...", flush=True)
    orig, sal = create_dummy_images()
    
    print(f"Dummy images created: {orig}, {sal}", flush=True)
    print("Generating report...", flush=True)
    try:
        report_path = generate_report(orig, sal)
        print(f"Report generated successfully at: {report_path}")
        
        # Verify content
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        checks = [
            "Executive Summary",
            "Attention Score",
            "Visual Clutter",
            "Cognitive Load",
            "Strategic Action Roadmap",
            "Methodology"
        ]
        
        for check in checks:
            if check in content:
                print(f"[PASS] Found section: {check}")
            else:
                print(f"[FAIL] Missing section: {check}")
                
    except Exception as e:
        print(f"Report generation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_generation()
