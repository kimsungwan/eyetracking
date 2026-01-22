import os
import json
import shutil
import uuid
from datetime import datetime
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import pydantic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import both models
from saliency_model import SaliencyModel as OriginalModel
from saliency_model_enhanced import SaliencyModel as EnhancedModel
from report_generator import generate_report

app = FastAPI(title="UVolution AI API")

# Get allowed origins from environment variable (comma-separated)
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

# Configure CORS to allow requests from Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories for uploads, outputs, and reports
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# Mount these directories as static so frontend can access generated images/reports
# In a production env, these should be uploaded to S3/Cloud Storage.
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")
app.mount("/reports", StaticFiles(directory="reports"), name="reports")

# === MODEL SELECTION ===
USE_ENHANCED = True

# Initialize model
if USE_ENHANCED:
    print("=" * 60)
    print("UVOLUTION AI - ENHANCED MODE (API)")
    print("=" * 60)
    model = EnhancedModel(enhanced_mode=True)
else:
    print("=" * 60)
    print("UVOLUTION AI - STANDARD MODE (API)")
    print("=" * 60)
    model = OriginalModel()

@app.get("/")
async def health_check():
    return {"status": "healthy", "service": "UVolution AI API"}

@app.post("/analyze")
async def analyze_image(plan: str = "free", file: UploadFile = File(...)):
    try:
        # Save uploaded file
        os.makedirs("uploads", exist_ok=True)
        
        # Generate unique filename using UUID
        file_extension = os.path.splitext(file.filename)[1]
        if not file_extension:
            file_extension = ".png"
            
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_location = f"uploads/{unique_filename}"
        
        # Generate timestamp for report filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Convert to PNG to ensure compatibility with OpenCV (handles animated WebP, etc.)
        try:
            from PIL import Image
            img = Image.open(file_location)
            img = img.convert('RGB') # Convert to RGB (removes alpha/animation)
            
            # Create new PNG filename
            png_filename = os.path.splitext(unique_filename)[0] + ".png"
            png_location = f"uploads/{png_filename}"
            
            # Save as PNG
            img.save(png_location, "PNG")
            
            # Update file_location to point to the PNG
            file_location = png_location
            print(f"Converted to PNG: {file_location}")
            
        except Exception as e:
            print(f"Error converting image: {e}")
            # Continue with original file if conversion fails (might fail later in OpenCV)

        # Process image
        print(f"Processing file: {file_location} (Plan: {plan})")
        if os.path.exists(file_location):
             print(f"File size: {os.path.getsize(file_location)} bytes")
        else:
             print("File does not exist!")

        saliency_map_path = model.predict(file_location)
        
        # Generate report
        report_path, ia_structure, redesign_suggestion, marketing_consultation, report_metrics = generate_report(file_location, saliency_map_path, timestamp=timestamp, plan=plan)
        
        # Return absolute URLs or relative paths that the frontend can construct
        # Use environment variable for base URL (Railway will provide the deployed URL)
        base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        
        return {
            "success": True,
            "original_image": f"{base_url}/{file_location.replace(os.sep, '/')}",
            "saliency_map": f"{base_url}/{saliency_map_path.replace(os.sep, '/')}",
            "report": f"{base_url}/{report_path.replace(os.sep, '/')}",
            "ia_structure": ia_structure,
            "redesign_suggestion": redesign_suggestion,
            "marketing_consultation": marketing_consultation,
            "metrics": report_metrics
        }
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return {"success": False, "error": str(e)}

class UrlRequest(pydantic.BaseModel):
    url: str
    plan: str = "free"

@app.post("/analyze-url")
async def analyze_url(request: UrlRequest):
    try:
        from screenshot_utils import capture_screenshot
        
        url = request.url
        plan = request.plan
        
        if not url.startswith("http"):
            url = "https://" + url
            
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}.png"
        file_location = f"uploads/{unique_filename}"
        
        # Capture screenshot
        print(f"Capturing screenshot for: {url}")
        success = capture_screenshot(url, file_location)
        
        if not success:
             return {"success": False, "error": "Failed to capture screenshot"}
             
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Process image using existing pipeline
        print(f"Processing screenshot: {file_location} (Plan: {plan})")
        saliency_map_path = model.predict(file_location)
        
        # Generate report
        report_path, ia_structure, redesign_suggestion, marketing_consultation, report_metrics = generate_report(file_location, saliency_map_path, timestamp=timestamp, plan=plan)
        
        base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        
        return {
            "success": True,
            "original_image": f"{base_url}/{file_location.replace(os.sep, '/')}",
            "saliency_map": f"{base_url}/{saliency_map_path.replace(os.sep, '/')}",
            "report": f"{base_url}/{report_path.replace(os.sep, '/')}",
            "ia_structure": ia_structure,
            "redesign_suggestion": redesign_suggestion,
            "marketing_consultation": marketing_consultation,
            "metrics": report_metrics
        }
    except Exception as e:
        print(f"Error processing URL: {str(e)}")
        return {"success": False, "error": str(e)}

@app.delete("/reports/{filename}")
async def delete_report(filename: str):
    try:
        # Define paths to delete
        # Filename is expected to be the base name (e.g., "uuid.png")
        
        # 1. Original Image (uploads/)
        original_path = f"uploads/{filename}"
        
        # 2. Saliency Map (outputs/)
        # Saliency map usually has "saliency_" prefix
        saliency_path = f"outputs/saliency_{filename}"
        
        # 3. HTML Report (reports/)
        # Report usually has "report_" prefix and .html extension
        # We might need to find the matching report file if the exact name isn't known,
        # but typically the report filename contains the original filename or UUID.
        # Based on report_generator.py: f"reports/report_{filename}_{timestamp}.html"
        # Since we might not have the timestamp, we can search for it or expect the full report filename to be passed?
        # Ideally, the Next.js backend should pass the exact paths or filenames.
        # Let's assume the frontend/Next.js passes the exact filenames for simplicity, 
        # OR we search for files containing the UUID.
        
        # Let's simplify: The Next.js backend has the full paths stored in the DB.
        # It can pass the filenames extracted from those paths.
        # However, the current route definition takes a single {filename}.
        # Let's change the strategy: Accept a JSON body with the list of files to delete.
        pass
    except Exception as e:
        return {"success": False, "error": str(e)}

class DeleteRequest(pydantic.BaseModel):
    files: list[str]



@app.post("/delete-files")
async def delete_files(request: DeleteRequest):
    deleted = []
    errors = []
    
    for file_path in request.files:
        # Security check: prevent directory traversal
        if ".." in file_path or file_path.startswith("/"):
             errors.append(f"Invalid path: {file_path}")
             continue
             
        # Normalize path separators
        safe_path = file_path.replace("/", os.sep).replace("\\", os.sep)
        
        # Ensure we are only deleting from allowed directories
        allowed_dirs = ["uploads", "outputs", "reports"]
        if not any(safe_path.startswith(d) for d in allowed_dirs):
             errors.append(f"Unauthorized directory: {file_path}")
             continue

        if os.path.exists(safe_path):
            try:
                os.remove(safe_path)
                deleted.append(file_path)
                print(f"Deleted: {safe_path}")
            except Exception as e:
                errors.append(f"Failed to delete {file_path}: {str(e)}")
        else:
            errors.append(f"File not found: {file_path}")
            
            return {"success": True, "deleted": deleted, "errors": errors}
    
    return {"success": True, "deleted": deleted, "errors": errors}

@app.get("/marketing-principles")
async def get_marketing_principles():
    try:
        json_path = os.path.join("knowledge_data", "knowledge.json")
        if not os.path.exists(json_path):
            return {"success": False, "error": "Knowledge database not found"}
            
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
