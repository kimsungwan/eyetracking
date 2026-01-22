import os
import google.generativeai as genai
from PIL import Image
import json

# Configure Gemini API
# Ensure GOOGLE_API_KEY is set in environment variables
GENAI_API_KEY = os.getenv("GOOGLE_API_KEY")
if GENAI_API_KEY:
    genai.configure(api_key=GENAI_API_KEY)

def analyze_ia_structure(image_path):
    """
    Analyzes the UI image and extracts the Information Architecture (IA) as a JSON tree.
    """
    if not GENAI_API_KEY:
        print("Warning: GOOGLE_API_KEY not found. Skipping IA analysis.")
        return None

    try:
        model = genai.GenerativeModel('gemini-2.5-flash-lite-preview-09-2025')
        img = Image.open(image_path)
        
        prompt = """
        Analyze this UI screenshot and extract its Information Architecture (IA) into a hierarchical JSON structure.
        
        The JSON should have a root node representing the page.
        Each node should have:
        - "label": A short descriptive name of the component/section (e.g., "Header", "Navigation", "Hero Section", "CTA Button").
        - "type": The type of element (e.g., "section", "button", "text", "image", "input").
        - "children": An array of child nodes.
        
        Focus on the logical structure and hierarchy.
        Return ONLY the JSON string, no markdown formatting.
        """
        
        response = model.generate_content([prompt, img])
        
        # Clean up response if it contains markdown code blocks
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
            
        return json.loads(text)
    except Exception as e:
        print(f"Error analyzing IA structure: {e}")
        return None

def generate_redesigned_ui(image_path, heatmap_path, analysis_summary):
    """
    Generates a redesigned UI image based on the original image, heatmap, and analysis.
    Note: This uses Gemini 1.5 Pro to generate a *description* of the redesign, 
    and potentially an image generation model if available (e.g. Imagen).
    For now, we will return a detailed text description of the redesign 
    and a placeholder for the image generation logic.
    """
    if not GENAI_API_KEY:
        print("Warning: GOOGLE_API_KEY not found. Skipping UI redesign.")
        return None

    try:
        model = genai.GenerativeModel('gemini-2.5-flash-lite-preview-09-2025')
        img = Image.open(image_path)
        heatmap = Image.open(heatmap_path)
        
        prompt = f"""
        You are an expert UI/UX Designer.
        I will provide you with:
        1. An original UI screenshot.
        2. An attention heatmap (where red/warm colors indicate high attention).
        3. An analysis summary: "{analysis_summary}"
        
        Your task is to propose a Redesign to improve the UX.
        
        1. Critique the current design based on the heatmap (e.g., is the user looking at the right things?).
        2. Describe a Redesigned Version that fixes these issues.
        3. Generate a prompt that could be used by an image generation model to create this new UI.
        
        Return the result as JSON:
        {{
            "critique": "...",
            "redesign_description": "...",
            "image_gen_prompt": "..."
        }}
        """
        
        response = model.generate_content([prompt, img, heatmap])
        
        # Clean up response
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
            
        return json.loads(text)
    except Exception as e:
        print(f"Error generating redesign suggestion: {e}")
        return None
