import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env explicitly
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"Loaded API Key: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")

if not api_key:
    print("❌ Error: GOOGLE_API_KEY is missing.")
    exit(1)

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3-pro-preview')
    response = model.generate_content("Hello, are you working?")
    print(f"✅ Success! Gemini responded: {response.text}")
except Exception as e:
    print(f"❌ API Call Failed: {str(e)}")
