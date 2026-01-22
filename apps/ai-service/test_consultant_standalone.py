import os
import json
from dotenv import load_dotenv
from consultant import generate_marketing_consultation

# Load .env
load_dotenv()

# Paths
original_image = "test_ui_design_1764094100664.png"
saliency_map = "outputs/saliency_test_ui_design_1764094100664.png"

print(f"Testing Marketing Consultant with:")
print(f"- Original: {original_image}")
print(f"- Heatmap: {saliency_map}")

if not os.path.exists(original_image):
    print(f"Error: Original image not found at {original_image}")
    exit(1)
if not os.path.exists(saliency_map):
    print(f"Error: Saliency map not found at {saliency_map}")
    exit(1)

try:
    print("\n--- Running Analysis (This may take 10-20 seconds) ---")
    result = generate_marketing_consultation(original_image, saliency_map)
    
    print("\n--- Analysis Result ---")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
except Exception as e:
    print(f"\nError during analysis: {e}")
