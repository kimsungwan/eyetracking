import os
from PIL import Image

directory = r"c:\Users\nocti\.gemini\antigravity\scratch\koreansaas\apps\client\public\images\docs"

for filename in os.listdir(directory):
    if filename.endswith(".png"):
        img_path = os.path.join(directory, filename)
        img = Image.open(img_path)
        webp_path = os.path.splitext(img_path)[0] + ".webp"
        img.save(webp_path, "WEBP")
        print(f"Converted {filename} to WebP")
        os.remove(img_path)
        print(f"Deleted {filename}")
