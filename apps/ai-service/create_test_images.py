import cv2
import numpy as np
import os

def create_test_images():
    os.makedirs("tests/images", exist_ok=True)
    
    # 1. Minimal UI (White bg, one button)
    img_min = np.ones((600, 800, 3), dtype=np.uint8) * 255
    # Add a blue button
    cv2.rectangle(img_min, (300, 250), (500, 350), (230, 100, 50), -1)
    # Add simple text
    cv2.putText(img_min, "Click Me", (340, 310), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imwrite("tests/images/minimal_ui.png", img_min)
    
    # 2. Marketing Banner (Colorful, gradients, text)
    img_ban = np.zeros((600, 800, 3), dtype=np.uint8)
    # Gradient bg
    for i in range(600):
        img_ban[i, :] = (i % 255, (i*2) % 255, 255 - (i % 255))
    # Add many shapes
    for i in range(20):
        cv2.circle(img_ban, (np.random.randint(0, 800), np.random.randint(0, 600)), np.random.randint(10, 50), (np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255)), -1)
    # Add text
    cv2.putText(img_ban, "BIG SALE!", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5)
    cv2.putText(img_ban, "50% OFF", (150, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 3)
    cv2.imwrite("tests/images/marketing_banner.jpg", img_ban)
    
    # 3. Analytics Dashboard (Grid, charts)
    img_dash = np.ones((600, 800, 3), dtype=np.uint8) * 240
    # Sidebar
    cv2.rectangle(img_dash, (0, 0), (200, 600), (50, 50, 50), -1)
    # Cards
    for y in range(50, 550, 150):
        for x in range(250, 750, 240):
            cv2.rectangle(img_dash, (x, y), (x+200, y+120), (255, 255, 255), -1)
            # Chart lines
            pts = np.array([[x+10, y+100], [x+50, y+80], [x+100, y+90], [x+150, y+40], [x+190, y+20]], np.int32)
            cv2.polylines(img_dash, [pts], False, (0, 200, 0), 2)
    cv2.imwrite("tests/images/analytics_dashboard.png", img_dash)
    
    # 4. Text Heavy (Rows of text)
    img_text = np.ones((600, 800, 3), dtype=np.uint8) * 255
    for y in range(50, 550, 20):
        cv2.putText(img_text, "This is a line of text representing content density in a typical article layout.", (50, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.imwrite("tests/images/text_heavy_article.png", img_text)
    
    print("Test images created.")

if __name__ == "__main__":
    create_test_images()
