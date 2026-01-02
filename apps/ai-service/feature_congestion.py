"""
Feature Congestion Module
Approximates Rosenholtz et al. (2007) Feature Congestion model for Visual Clutter.
Reference: Rosenholtz, R., Li, Y., & Nakano, L. (2007). Measuring visual clutter.

This module computes local feature covariance in color, contrast, and orientation
to estimate the difficulty of visual search (clutter).
"""

import cv2
import numpy as np

def compute_local_variance(image_channel, window_size=16):
    """
    Computes local variance using the E[X^2] - E[X]^2 trick with box filters.
    Fast approximation for sliding window variance.
    """
    # Convert to float for precision
    img = image_channel.astype(np.float32)
    
    # E[X]
    mean = cv2.blur(img, (window_size, window_size))
    
    # E[X^2]
    mean_sq = cv2.blur(img**2, (window_size, window_size))
    
    # Var(X) = E[X^2] - E[X]^2
    variance = mean_sq - mean**2
    
    # Avoid negative values due to float precision
    variance[variance < 0] = 0
    
    return variance

def compute_orientation_map(luminance):
    """
    Computes a simple orientation map using Sobel gradients.
    Returns the angle of gradients (0-180 degrees).
    """
    gx = cv2.Sobel(luminance, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(luminance, cv2.CV_32F, 0, 1, ksize=3)
    
    mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)
    
    # We only care about orientation, not direction (0-180)
    angle = np.mod(angle, 180)
    
    # Mask out low magnitude areas (noise)
    mask = mag < 10
    angle[mask] = 0
    
    return angle

def normalize_map(feature_map, mode="percentile"):
    """
    Normalizes a feature map to 0-100 scale.
    """
    if mode == "zscore":
        mu = np.mean(feature_map)
        sigma = np.std(feature_map) + 1e-8
        z = (feature_map - mu) / sigma
        
        # Clip outliers [-3, 3]
        z = np.clip(z, -3, 3)
        
        # Map to 0-100
        norm = (z + 3) / 6 * 100
        
    else: # percentile (default)
        p5 = np.percentile(feature_map, 5)
        p95 = np.percentile(feature_map, 95)
        
        norm = (feature_map - p5) / (p95 - p5 + 1e-8)
        norm = np.clip(norm, 0, 1) * 100
        
    return np.clip(norm, 0, 100)

def compute_feature_congestion(image_path, window_size=16):
    """
    Main function to compute Rosenholtz-style Feature Congestion.
    
    Returns:
        dict: {
            "complexity_score": float (0-100),
            "contrast_variance": float,
            "orientation_variance": float,
            "color_variance": float,
            "grade": str (A/B/C/D)
        }
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")
        
    # 1. Color Variance (CIELAB)
    # Convert to LAB to separate luminance (L) from color (a, b)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)
    
    var_a = compute_local_variance(a_channel, window_size)
    var_b = compute_local_variance(b_channel, window_size)
    
    # Combine color variance
    color_var_map = (var_a + var_b) / 2.0
    
    # 2. Contrast Variance (Luminance)
    contrast_var_map = compute_local_variance(l_channel, window_size)
    
    # 3. Orientation Variance
    # Compute orientation on L channel
    orientation_map = compute_orientation_map(l_channel)
    orientation_var_map = compute_local_variance(orientation_map, window_size)
    
    # 4. Normalization & Combination
    # Normalize each map individually first to balance contributions
    norm_color = normalize_map(color_var_map, mode="percentile")
    norm_contrast = normalize_map(contrast_var_map, mode="percentile")
    norm_orient = normalize_map(orientation_var_map, mode="percentile")
    
    # Weighted Combination (Rosenholtz principles)
    # Weights: Contrast usually dominates, but we use balanced weights as requested
    w1, w2, w3 = 0.34, 0.33, 0.33
    
    fc_map = (w1 * norm_contrast) + (w2 * norm_orient) + (w3 * norm_color)
    
    # Final Score: Mean of the combined map
    # This represents the "average local clutter" across the image
    complexity_score = np.mean(fc_map)
    
    # Grading
    if complexity_score <= 35:
        grade = "A"
        interpretation = "Minimalist - Very low visual clutter"
    elif complexity_score <= 55:
        grade = "B"
        interpretation = "Balanced - Moderate visual complexity"
    elif complexity_score <= 75:
        grade = "C"
        interpretation = "High - Visually busy"
    else:
        grade = "D"
        interpretation = "Excessive - Cognitive overload likely"
        
    return {
        "complexity_score": round(float(complexity_score), 1),
        "contrast_variance": round(float(np.mean(norm_contrast)), 1),
        "orientation_variance": round(float(np.mean(norm_orient)), 1),
        "color_variance": round(float(np.mean(norm_color)), 1),
        "grade": grade,
        "interpretation": interpretation
    }

if __name__ == "__main__":
    # Simple test
    print("Feature Congestion Module Loaded.")
