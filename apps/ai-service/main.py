import os
import shutil
import uuid
from datetime import datetime
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import both models
from saliency_model import SaliencyModel as OriginalModel
from saliency_model_enhanced import SaliencyModel as EnhancedModel
from report_generator import generate_report

app = FastAPI(title="UVolution AI API")

# Configure CORS to allow requests from Next.js (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
async def analyze_image(file: UploadFile = File(...)):
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
        print(f"Processing file: {file_location}")
        if os.path.exists(file_location):
             print(f"File size: {os.path.getsize(file_location)} bytes")
        else:
             print("File does not exist!")

        saliency_map_path = model.predict(file_location)
        
        # Generate report
        report_path = generate_report(file_location, saliency_map_path, timestamp=timestamp)
        
        # Return absolute URLs or relative paths that the frontend can construct
        # Assuming the API is running on localhost:8000
        base_url = "http://localhost:8000"
        
        return {
            "success": True,
            "original_image": f"{base_url}/{file_location.replace(os.sep, '/')}",
            "saliency_map": f"{base_url}/{saliency_map_path.replace(os.sep, '/')}",
            "report": f"{base_url}/{report_path.replace(os.sep, '/')}"
        }
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
