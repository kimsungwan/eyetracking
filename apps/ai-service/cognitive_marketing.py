"""
Cognitive Marketing Analysis Module
Extracts marketing-relevant cognitive engineering insights from UI images.
Strictly adheres to visually verifiable data (Saliency, Edges, Colors).
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple

def analyze_whitespace_ratio(image_path: str) -> Dict:
    """
    Analyze whitespace/negative space ratio.
    Ground Truth: Pixel intensity analysis.
    Scientific Basis: Lin (2004) - Whitespace improves comprehension.
    """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Threshold to identify "empty" areas (near white/light)
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    
    whitespace_pixels = np.count_nonzero(binary)
    total_pixels = gray.size
    whitespace_ratio = (whitespace_pixels / total_pixels) * 100
    
    # Interpretation
    if whitespace_ratio >= 40:
        interpretation = "High - Open, breathable layout"
        score = "A"
    elif whitespace_ratio >= 25:
        interpretation = "Moderate - Balanced density"
        score = "B"
    elif whitespace_ratio >= 15:
        interpretation = "Low - Dense information packing"
        score = "C"
    else:
        interpretation = "Very Low - High visual density"
        score = "D"
    
    return {
        "whitespace_ratio": round(whitespace_ratio, 1),
        "interpretation": interpretation,
        "score": score,
        "recommendation": "Maintain 30-50% whitespace to reduce cognitive load (Lin, 2004)."
    }


def detect_cta_placement(image_path: str, saliency_map_path: str) -> Dict:
    """
    Detect likely CTA button positions using visual saliency and saturation.
    Ground Truth: Saliency map intensity + Color saturation.
    """
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    
    # Load saliency map
    saliency = cv2.imread(saliency_map_path, cv2.IMREAD_GRAYSCALE)
    
    # Identify highly saturated regions (likely CTAs)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    saturation = hsv[:, :, 1]
    
    # High saturation + high value = likely CTA
    _, sat_mask = cv2.threshold(saturation, 100, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(sat_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter by size (typical button size relative to viewport)
    min_area = (w * h) * 0.001  # 0.1% of image
    max_area = (w * h) * 0.05   # 5% of image
    
    ctas = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if min_area < area < max_area:
            x, y, w_btn, h_btn = cv2.boundingRect(cnt)
            
            # Calculate position metrics
            y_position = y / h
            x_position = x / w
            
            # Check saliency at CTA location
            cta_saliency = np.mean(saliency[y:y+h_btn, x:x+w_btn])
            
            ctas.append({
                "position": (x, y),
                "size": (w_btn, h_btn),
                "y_ratio": round(y_position, 2),
                "x_ratio": round(x_position, 2),
                "saliency": round(cta_saliency, 1)
            })
    
    # Evaluate placement based on visual prominence
    recommendations = []
    
    if len(ctas) == 0:
        recommendations.append("No highly saturated elements detected. Ensure CTA contrasts with background.")
    else:
        # Sort by saliency
        ctas.sort(key=lambda x: x['saliency'], reverse=True)
        top_cta = ctas[0]
        
        if top_cta["saliency"] < 100:
             recommendations.append("Primary CTA has low visual weight. Increase contrast or size.")
        
        if top_cta["y_ratio"] > 0.9:
             recommendations.append("Primary CTA is located at the very bottom. Ensure visibility above the fold.")

    return {
        "cta_count": len(ctas),
        "cta_details": ctas[:3],
        "recommendations": recommendations if recommendations else ["CTA has strong visual presence."]
    }


def analyze_visual_hierarchy(image_path: str) -> Dict:
    """
    Analyze size-based visual hierarchy.
    Ground Truth: Contour area distribution.
    Scientific Basis: Gestalt Principle of Size.
    """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Edge detection to find content blocks
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    areas = [cv2.contourArea(cnt) for cnt in contours if cv2.contourArea(cnt) > 100]
    
    if len(areas) < 2:
        return {
            "hierarchy_score": 50,
            "interpretation": "Uniform element sizes",
            "recommendation": "Create variation in element sizes to guide the eye."
        }
    
    # Sort areas
    areas_sorted = sorted(areas, reverse=True)
    
    # Calculate ratio of largest (Heading) to median (Body)
    largest = areas_sorted[0]
    median = np.median(areas_sorted)
    
    hierarchy_ratio = largest / (median + 1e-8)
    
    # Score
    if hierarchy_ratio >= 8:
        score = 95
        interpretation = "Strong - Clear focal points"
    elif hierarchy_ratio >= 5:
        score = 75
        interpretation = "Moderate - Distinguishable levels"
    else:
        score = 40
        interpretation = "Weak - Flat hierarchy"
    
    return {
        "hierarchy_score": score,
        "hierarchy_ratio": round(hierarchy_ratio, 2),
        "interpretation": interpretation,
        "recommendation": "Ensure primary elements are significantly larger than secondary ones."
    }


# Updated to Rosenholtz-style Feature Congestion Approximation
# Reference: Rosenholtz, R., Li, Y., & Nakano, L. (2007). Measuring visual clutter.

from feature_congestion import compute_feature_congestion

def analyze_visual_complexity(image_path: str) -> Dict:
    """
    Analyze Visual Complexity using Rosenholtz's Feature Congestion model.
    Replaces legacy edge density method.
    """
    try:
        # Use the new Feature Congestion module
        fc_data = compute_feature_congestion(image_path)
        
        return {
            "complexity_score": fc_data["complexity_score"],
            "grade": fc_data["grade"],
            "interpretation": fc_data["interpretation"],
            "details": {
                "contrast_var": fc_data["contrast_variance"],
                "orientation_var": fc_data["orientation_variance"],
                "color_var": fc_data["color_variance"]
            },
            "recommendation": "High feature congestion increases search time. Simplify visual noise."
        }
    except Exception as e:
        print(f"Feature Congestion analysis failed: {e}")
        # Fallback to simple edge density if FC fails
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        edge_density = np.count_nonzero(edges) / edges.size
        score = min(100, edge_density * 500)
        
        return {
            "complexity_score": round(score, 1),
            "grade": "C" if score > 50 else "B",
            "interpretation": "Fallback: Edge Density Estimate",
            "recommendation": "Simplify layout."
        }

def analyze_saliency_distribution(saliency_map_path: str) -> Dict:
    """
    Analyze how attention is distributed across the layout.
    Replaces 'Scroll Depth Prediction' with verifiable attention distribution.
    Ground Truth: Saliency map pixel intensity.
    """
    saliency = cv2.imread(saliency_map_path, cv2.IMREAD_GRAYSCALE)
    h, w = saliency.shape
    
    # Divide into vertical thirds
    third_h = h // 3
    top_sal = np.mean(saliency[:third_h, :])
    mid_sal = np.mean(saliency[third_h:2*third_h, :])
    bottom_sal = np.mean(saliency[2*third_h:, :])
    
    total = top_sal + mid_sal + bottom_sal + 1e-8
    
    distribution = {
        "top": round((top_sal / total) * 100, 1),
        "middle": round((mid_sal / total) * 100, 1),
        "bottom": round((bottom_sal / total) * 100, 1)
    }
    
    if distribution["top"] > 60:
        pattern = "Top-Heavy (Above the fold focus)"
    elif distribution["bottom"] > 30:
        pattern = "Distributed (Strong footer engagement)"
    else:
        pattern = "Balanced Flow"
        
    return {
        "distribution": distribution,
        "pattern": pattern,
        "recommendation": "Ensure key value propositions align with high-saliency regions."
    }


def generate_cognitive_marketing_analysis(image_path: str, saliency_map_path: str) -> Dict:
    """
    Main function to run all cognitive marketing analyses.
    """
    return {
        "whitespace": analyze_whitespace_ratio(image_path),
        "cta_placement": detect_cta_placement(image_path, saliency_map_path),
        "visual_hierarchy": analyze_visual_hierarchy(image_path),
        "visual_complexity": analyze_visual_complexity(image_path),
        "saliency_distribution": analyze_saliency_distribution(saliency_map_path)
    }

if __name__ == "__main__":
    print("Cognitive Marketing Analysis Module loaded successfully.")
