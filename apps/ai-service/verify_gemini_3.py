import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found.")
    exit(1)

print(f"Using API Key: {api_key[:5]}...{api_key[-5:]}")

try:
    genai.configure(api_key=api_key)
    # Using the specific model requested
    model = genai.GenerativeModel('gemini-3-pro-preview')
    
    print("Sending request to Gemini 3 Pro...")
    response = model.generate_content("100자 이내로 짧게 자기소개를 해줘. 한국어로.")
    
    print("\n--- Gemini Response ---")
    print(response.text)
    print("-----------------------")
    
except Exception as e:
    print(f"\nError: {str(e)}")
