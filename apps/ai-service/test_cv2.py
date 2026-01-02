import sys
print("Python version:", sys.version)
try:
    import cv2
    print("cv2 imported successfully")
except ImportError as e:
    print(f"cv2 import failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
