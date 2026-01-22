import os
import json
import glob
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY not found in .env file.")
    exit(1)

genai.configure(api_key=GOOGLE_API_KEY)

# Configuration
PDF_DIR = "knowledge_data/raw_pdfs"
KNOWLEDGE_FILE = "knowledge_data/knowledge.json"
CHARTS_FILE = "knowledge_data/charts.json"

def ingest_pdfs():
    print(f"🔍 Scanning {PDF_DIR} for PDFs...")
    pdf_files = glob.glob(os.path.join(PDF_DIR, "*.pdf"))
    
    if not pdf_files:
        print("⚠️ No PDF files found. Please add PDFs to the 'knowledge_data/raw_pdfs' folder.")
        return

    # Load existing data
    try:
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            knowledge_db = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        knowledge_db = []

    try:
        with open(CHARTS_FILE, "r", encoding="utf-8") as f:
            charts_db = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        charts_db = []

    # Initialize Gemini Model (Using latest Gemini 3 Pro for superior reasoning)
    model = genai.GenerativeModel('gemini-2.5-flash-lite-preview-09-2025')

    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        print(f"\n📄 Processing: {filename}...")
        
        try:
            # Upload file to Gemini
            sample_file = genai.upload_file(path=pdf_path, display_name=filename)
            print(f"   - Uploaded to Gemini (URI: {sample_file.uri})")
            
            # Wait for processing
            while sample_file.state.name == "PROCESSING":
                print("   - Processing PDF...")
                time.sleep(2)
                sample_file = genai.get_file(sample_file.name)
                
            if sample_file.state.name == "FAILED":
                print("   - PDF processing failed.")
                continue

            # Prompt for Multimodal Extraction
            prompt = """
            Analyze this PDF document as a Marketing Expert. 
            
            Task 1: Extract key marketing concepts, theories, or psychological principles.
            Format as a JSON list of objects with these fields:
            - id: unique_snake_case_id
            - concept: Name of the concept
            - category: e.g., "Behavioral Economics", "UX Strategy"
            - definition: A clear, beginner-friendly explanation (expert-to-non-expert style).
            - visual_triggers: List of visual elements that trigger this concept (e.g., "pricing table", "hero image").
            - actionable_advice: List of specific, actionable steps to apply this concept.
            - case_study: A real-world example mentioned in the text or general knowledge.
            
            Task 2: Extract any charts, graphs, or data tables.
            Format as a separate JSON list of objects with these fields:
            - id: unique_chart_id
            - title: Title of the chart/graph
            - type: e.g., "Bar Chart", "Line Graph", "Table"
            - key_insight: The main takeaway or trend shown in the data.
            - data_summary: A text summary of the data points.
            - relevance: How this data applies to marketing optimization.

            Return the response as a single valid JSON object with two keys: "concepts" and "charts".
            Do not use markdown code blocks. Just raw JSON.
            """

            response = model.generate_content([sample_file, prompt])
            
            # Parse Response
            try:
                # Clean up markdown if present
                text = response.text.replace("```json", "").replace("```", "").strip()
                result = json.loads(text)
                
                new_concepts = result.get("concepts", [])
                new_charts = result.get("charts", [])
                
                print(f"   - Extracted {len(new_concepts)} concepts and {len(new_charts)} charts.")
                
                # Merge Data (Simple append for now, could add dedup logic)
                knowledge_db.extend(new_concepts)
                charts_db.extend(new_charts)
                
            except json.JSONDecodeError as e:
                print(f"   - Failed to parse JSON response: {e}")
                print(f"   - Raw response: {response.text[:200]}...")

        except Exception as e:
            print(f"   - Error processing {filename}: {str(e)}")

    # Save updated databases
    with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
        json.dump(knowledge_db, f, indent=2, ensure_ascii=False)
        
    with open(CHARTS_FILE, "w", encoding="utf-8") as f:
        json.dump(charts_db, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Ingestion Complete!")
    print(f"   - Total Concepts: {len(knowledge_db)}")
    print(f"   - Total Charts: {len(charts_db)}")
    print("   - Run 'python knowledge_base.py' to update the vector database.")

if __name__ == "__main__":
    ingest_pdfs()
