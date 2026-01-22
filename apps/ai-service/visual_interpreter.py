import os
import google.generativeai as genai
from PIL import Image

# Configure Gemini API
# Assumes GOOGLE_API_KEY is set in environment variables
if "GOOGLE_API_KEY" in os.environ:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def interpret_visual_data(original_image_path: str, heatmap_path: str) -> str:
    """
    Analyzes the original image and heatmap using Gemini Vision to describe user behavior.
    Returns a text description of the gaze path and attention points.
    """
    if "GOOGLE_API_KEY" not in os.environ:
        return "Error: GOOGLE_API_KEY not found. Cannot perform visual interpretation."

    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash-lite-preview-09-2025')
        
        original_img = Image.open(original_image_path)
        heatmap_img = Image.open(heatmap_path)
        
        prompt = """
        You are an expert UX researcher analyzing eye-tracking data.
        
        Input:
        1. The original UI design.
        2. A heatmap overlay showing where users looked (red/hot areas = high attention, blue/cold = low attention).
        
        Task:
        Describe the user's viewing behavior in detail. Focus on:
        - What elements grabbed the most attention? (Headlines, Images, CTAs?)
        - What important elements were ignored or skipped?
        - Is the gaze path linear, scattered, or focused?
        - Does the user follow any common patterns (F-pattern, Z-pattern)?
        
        Output Format:
        Provide a concise but detailed paragraph describing the visual behavior. Do not offer solutions yet, just observations.
        """
        
        response = model.generate_content([prompt, original_img, heatmap_img])
        return response.text
        
    except Exception as e:
        print(f"Error in visual interpretation: {str(e)}")
        return f"Visual interpretation failed: {str(e)}"
