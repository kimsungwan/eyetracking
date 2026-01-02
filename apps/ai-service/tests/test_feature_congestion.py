import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from feature_congestion import compute_feature_congestion
import cv2

def test_feature_congestion():
    images = [
        "tests/images/minimal_ui.png",
        "tests/images/marketing_banner.jpg",
        "tests/images/analytics_dashboard.png",
        "tests/images/text_heavy_article.png"
    ]
    
    print(f"{'Image':<30} | {'Score':<6} | {'Grade':<5} | {'Contrast':<8} | {'Orient':<8} | {'Color':<8}")
    print("-" * 80)
    
    for img_path in images:
        if not os.path.exists(img_path):
            print(f"Skipping {img_path} (not found)")
            continue
            
        try:
            res = compute_feature_congestion(img_path)
            print(f"{os.path.basename(img_path):<30} | {res['complexity_score']:<6} | {res['grade']:<5} | {res['contrast_variance']:<8} | {res['orientation_variance']:<8} | {res['color_variance']:<8}")
        except Exception as e:
            print(f"Error processing {img_path}: {e}")

if __name__ == "__main__":
    test_feature_congestion()
