# UI/UX Eye Tracking Datasets

This directory contains information and scripts to download state-of-the-art eye-tracking datasets specifically designed for User Interfaces (UI) and User Experience (UX) research.

## 1. UEyes (2024)
- **Description**: Large-scale dataset with 62 participants and 1,980 UI screenshots (Desktop, Mobile, Web, Poster).
- **Size**: ~20,000 saliency maps.
- **Source**: [Zenodo Record 8010312](https://zenodo.org/record/8010312)
- **Usage**: Best for general UI saliency validation.

## 2. WIC640 (2024/2025)
- **Description**: 640 web pages with eye-tracking data from 85 participants. Focuses on gender/age differences.
- **Source**: [NIH / Research Papers]
- **Usage**: Web-specific attention analysis.

## 3. Imp1k (UMSI Dataset)
- **Description**: 1000 designs (posters, infographics, ads, mobile UIs) with importance annotations.
- **Source**: [MIT CSAIL](http://people.csail.mit.edu/cfosco/umsi/)
- **Usage**: Graphic design and marketing material analysis.

## 4. SALICON
- **Description**: Large-scale dataset based on MS COCO, using mouse-tracking as a proxy for attention.
- **Source**: [SALICON.net](http://salicon.net/)
- **Usage**: Pre-training large models.

## How to Use
Run the `download_datasets.py` script to download these datasets to this directory.
```bash
python download_datasets.py
```
