# AI Eye-Tracking SaaS Implementation Plan

## Goal Description
Develop a Python-based Web SaaS that accepts an image input, applies AI-based saliency map eye-tracking technology, and generates a UX research report. The system will be delivered as a landing page with a functional demo.

## User Review Required
> [!IMPORTANT]
> **Model Selection**: We will use a pre-trained Saliency Map model (likely SAM-ResNet or a similar PyTorch implementation) trained on the SALICON dataset. The weights need to be downloaded.
> **Dataset**: The user requested to download datasets. The SALICON dataset is large (several GB). We will provide a script or instructions to download it, but we will primarily focus on downloading the *pre-trained model weights* which are sufficient for inference.

## Proposed Changes

### Backend (FastAPI)
#### [NEW] `main.py`
- Setup FastAPI app.
- Define `/upload` endpoint.
- Integrate Saliency Model inference.

#### [NEW] `saliency_model.py`
- Load the pre-trained PyTorch model.
- Preprocess input image (resize, normalize).
- Postprocess output (heatmap generation, overlay).

#### [NEW] `report_generator.py`
- Generate a PDF or HTML report containing:
    - Original Image.
    - Saliency Map.
    - Basic analytics (e.g., "Top 3 attention areas").

### Frontend (HTML/JS)
#### [NEW] `static/index.html`
- Landing page with "Hero" section.
- File upload area (Drag & Drop).
- Result display area.
- "Download Report" button.

#### [NEW] `static/style.css`
- Modern, premium design (Dark mode, gradients).

#### [NEW] `static/script.js`
- Handle file upload via AJAX/Fetch.
- Display loading state.
- Render results.

### Resources & Setup
#### [NEW] `resources.txt`
- List of all Python libraries.
- Links to model weights and datasets.

#### [NEW] `download_resources.py`
- Script to automatically download model weights if possible.

## Verification Plan

### Automated Tests
- **Unit Tests**: Test the `saliency_model.py` with a dummy image to ensure it returns a heatmap of correct shape.
- **API Tests**: Test `/upload` endpoint with `TestClient`.

### Manual Verification
- **Browser Testing**: Open `http://localhost:8000`, upload an image, and verify the heatmap looks reasonable (hotspots on salient objects).
- **Report Check**: Download the generated report and verify content.
