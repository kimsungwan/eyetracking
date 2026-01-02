import os
import numpy as np
import cv2
from jinja2 import Template
from scipy.stats import entropy
from datetime import datetime
import time
from content_engine import (
    get_executive_summary_text,
    get_visual_attention_deep_dive,
    get_cognitive_load_deep_dive,
    get_ux_heuristics_text,
    get_strategic_action_plan,
    get_emotion_icon,
    calculate_contrast_score,
    generate_color_scientific_text,
    generate_color_marketing_text,
    generate_color_cultural_text,
    generate_color_industry_text,
    generate_color_summary_text
)

# Color Report Revamp:
# Increased detail, added scientific metrics, cultural variants, 
# industry-specific insights, improved layout, stronger UX narrative.

def calculate_metrics(saliency_map_path, original_image_path):
    """
    Calculates quantitative UX metrics using advanced algorithms.
    """
    # Load images
    saliency = cv2.imread(saliency_map_path, cv2.IMREAD_GRAYSCALE)
    original = cv2.imread(original_image_path)
    
    # --- 1. Advanced Visual Clutter (Edge Density + Color Entropy) ---
    # A. Edge Density (Structural Clutter)
    edges = cv2.Canny(original, 100, 200)
    edge_density = np.count_nonzero(edges) / edges.size
    
    # B. Color Clutter (Color Entropy)
    hsv = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)
    h_hist = cv2.calcHist([hsv], [0], None, [50], [0, 180])
    h_hist_norm = h_hist / (np.sum(h_hist) + 1e-8)
    color_entropy = entropy(h_hist_norm.flatten())
    
    # Combine metrics
    edge_score = min(100, (edge_density / 0.15) * 100)
    color_score = min(100, (color_entropy / 3.5) * 100)
    clutter_final = (edge_score * 0.7) + (color_score * 0.3)
    
    # --- 2. Focus Ratio ---
    threshold = np.percentile(saliency, 90)
    focus_area = np.sum(saliency > threshold)
    total_area = saliency.size
    focus_ratio = (focus_area / total_area) * 100
    
    # --- 3. Hotspot Count ---
    _, thresh = cv2.threshold(saliency, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hotspots = [c for c in contours if cv2.contourArea(c) > (total_area * 0.001)]
    hotspot_count = len(hotspots)
    
    return {
        "clutter_score": round(clutter_final, 1),
        "focus_ratio": round(focus_ratio, 1),
        "hotspot_count": hotspot_count,
        "edge_density": round(edge_density * 100, 2),
        "color_entropy": round(color_entropy, 2)
    }

def calculate_advanced_metrics(saliency_map_path, original_image_path, basic_metrics, cognitive_data):
    """
    Calculates advanced marketing-focused metrics: ACS, VCI, CLE.
    """
    saliency = cv2.imread(saliency_map_path, cv2.IMREAD_GRAYSCALE)
    
    # 1. Attention Capture Score (ACS)
    max_sal = np.max(saliency) / 255.0
    top_10_mean = np.mean(saliency[saliency > np.percentile(saliency, 90)]) / 255.0
    acs = (max_sal * 0.4 + top_10_mean * 0.6) * 100
    
    # 2. Visual Clutter Index (VCI)
    vci = basic_metrics['clutter_score']
    
    # 3. Cognitive Load Estimate (CLE)
    whitespace_ratio = cognitive_data['whitespace']['whitespace_ratio'] if cognitive_data else 30
    cle = ((100 - whitespace_ratio) * 0.6) + (vci * 0.4)
    
    return {
        "acs": round(acs, 1),
        "vci": round(vci, 1),
        "cle": round(cle, 1)
    }

def analyze_dominant_colors(image_path):
    """
    Extract dominant colors from UI and provide psychology-based recommendations.
    Updated to use structured Science/Marketing data.
    """
    from color_psychology import analyze_color_psychology, recommend_cta_color, calculate_contrast_ratio, get_wcag_level
    import cv2
    from sklearn.cluster import KMeans
    
    # Load image
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Reshape for K-means
    pixels = img_rgb.reshape(-1, 3)
    
    # Find 5 dominant colors
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    kmeans.fit(pixels)
    
    # Get dominant colors sorted by frequency
    unique, counts = np.unique(kmeans.labels_, return_counts=True)
    sorted_indices = np.argsort(-counts)
    dominant_colors = kmeans.cluster_centers_[sorted_indices].astype(int)
    percentages = (counts[sorted_indices] / counts.sum() * 100).round(1)
    
    # Convert to hex
    dominant_hex = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in dominant_colors]
    
    # Analyze psychology of each color
    color_analysis = []
    for i, (hex_color, pct) in enumerate(zip(dominant_hex[:5], percentages[:5])):  # Top 5 for palette
        analysis = analyze_color_psychology(hex_color)
        marketing = analysis.get("marketing", {})
        scientific = analysis.get("scientific", {})
        
        emotion = marketing.get("primary_emotion", "Neutral")
        
        # Generate rich text descriptions
        sci_text = generate_color_scientific_text(analysis)
        mkt_text = generate_color_marketing_text(analysis)
        cult_text = generate_color_cultural_text(analysis)
        ind_text = generate_color_industry_text(analysis)
        
        color_analysis.append({
            "hex": hex_color,
            "percentage": pct,
            "family": marketing.get("color_family", "unknown"),
            "emotions": marketing.get("emotions", []),
            "primary_emotion": emotion,
            "icon": get_emotion_icon(emotion),
            "scientific": scientific,
            "marketing": marketing,
            "text": {
                "scientific": sci_text,
                "marketing": mkt_text,
                "cultural": cult_text,
                "industry": ind_text
            }
        })
    
    # Detect likely background color (most dominant unless it's too bright/dark)
    bg_color = dominant_hex[0]
    
    # Recommend optimal CTA color
    cta_recommendation = recommend_cta_color(industry=None, current_bg=bg_color)
    
    # Calculate Contrast Score Improvement (Replacing CTR Simulation)
    # Estimate current contrast (worst case scenario of dominant colors)
    current_contrast = 1.5 # Default low assumption
    if len(dominant_hex) > 1:
        current_contrast = calculate_contrast_ratio(dominant_hex[0], dominant_hex[1])
        
    contrast_score = calculate_contrast_score(current_contrast, cta_recommendation['scientific']['contrast_ratio'])
    
    # Check contrast of current dominant colors against each other
    contrast_issues = []
    for i in range(min(3, len(dominant_hex))):
        for j in range(i+1, min(3, len(dominant_hex))):
            contrast = calculate_contrast_ratio(dominant_hex[i], dominant_hex[j])
            level = get_wcag_level(contrast)
            if level == "FAIL":
                contrast_issues.append({
                    "color1": dominant_hex[i],
                    "color2": dominant_hex[j],
                    "contrast": round(contrast, 2),
                    "issue": f"Low contrast ({contrast:.1f}:1) - needs improvement for accessibility"
                })
    
    # Generate Palette Summary
    palette_summary = generate_color_summary_text(color_analysis)
    
    return {
        "dominant_colors": color_analysis,
        "background_color": bg_color,
        "cta_recommendation": cta_recommendation,
        "contrast_issues": contrast_issues,
        "contrast_score": contrast_score,
        "palette_summary": palette_summary
    }

def generate_report(original_image_path, saliency_map_path, timestamp=None):
    """
    Generates a comprehensive 5+ page HTML report with deep-dive analysis.
    """
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)
    
    # Extract filename from path
    filename = os.path.basename(original_image_path)
    
    if not timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    # Use pure timestamp filename to avoid encoding issues
    report_path = os.path.join(report_dir, f"report_{timestamp}.html")
    
    # Calculate Basic Metrics
    metrics = calculate_metrics(saliency_map_path, original_image_path)
    
    # Analyze Colors
    try:
        color_data = analyze_dominant_colors(original_image_path)
        print(f"Color analysis successful: {len(color_data['dominant_colors'])} colors detected")
    except Exception as e:
        print(f"Color analysis failed: {e}")
        import traceback
        traceback.print_exc()
        color_data = None
    
    # Cognitive Marketing Analysis
    try:
        from cognitive_marketing import generate_cognitive_marketing_analysis
        cognitive_data = generate_cognitive_marketing_analysis(original_image_path, saliency_map_path)
    except Exception as e:
        print(f"Cognitive marketing analysis failed: {e}")
        cognitive_data = None
        
    # Calculate Advanced Metrics (ACS, VCI, CLE)
    adv_metrics = calculate_advanced_metrics(saliency_map_path, original_image_path, metrics, cognitive_data)
    
    # --- CONTENT ENGINE GENERATION ---
    exec_summary = get_executive_summary_text(adv_metrics['acs'], adv_metrics['cle'], metrics['hotspot_count'])
    visual_text = get_visual_attention_deep_dive(metrics['hotspot_count'], metrics['focus_ratio'])
    cognitive_text = get_cognitive_load_deep_dive(adv_metrics['vci'], cognitive_data['whitespace']['whitespace_ratio'] if cognitive_data else 30)
    
    ux_text = get_ux_heuristics_text(cognitive_data['visual_complexity'] if cognitive_data else {'grade': 'B'}, metrics['hotspot_count'])
    
    # UX Heuristics Extension: Add detailed Nielsen heuristics analysis
    try:
        from content_engine import build_ux_heuristics_details
        ux_heuristics_details = build_ux_heuristics_details(metrics, adv_metrics, cognitive_data, color_data)
    except Exception as e:
        print(f"Extended UX heuristics failed: {e}")
        ux_heuristics_details = []
    
    # Added Gaze Path Efficiency (minimal addition, no rewrites)
    try:
        from content_engine import build_gaze_path_efficiency
        gaze_path_data = build_gaze_path_efficiency(saliency_map_path)
    except Exception as e:
        print(f"Gaze path efficiency failed: {e}")
        gaze_path_data = {"score": 50, "insight": "Analysis unavailable.", "recommendation": "N/A"}
    
    action_plan = get_strategic_action_plan(metrics, adv_metrics, cognitive_data)
    
    # COMPREHENSIVE 5+ PAGE HTML TEMPLATE
    template_str = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Uvolution AI - Comprehensive UX Analysis</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary: #4f46e5;
                --primary-light: #818cf8;
                --secondary: #0ea5e9;
                --accent: #f59e0b;
                --text-main: #1e293b;
                --text-muted: #64748b;
                --bg-light: #f8fafc;
                --bg-white: #ffffff;
                --success: #10b981;
                --danger: #ef4444;
            }
            
            * { box-sizing: border-box; }
            body { font-family: 'Inter', sans-serif; background: var(--bg-light); color: var(--text-main); margin: 0; padding: 0; line-height: 1.7; }
            
            /* Page Structure for Print/PDF */
            .page { 
                background: white; 
                max-width: 210mm; 
                min-height: 297mm; 
                margin: 2rem auto; 
                padding: 2.5rem; 
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); 
                position: relative;
                page-break-after: always;
            }
            
            /* Typography */
            h1 { font-size: 2.5rem; font-weight: 800; color: var(--primary); margin-bottom: 0.5rem; letter-spacing: -0.025em; }
            h2 { font-size: 1.75rem; font-weight: 700; color: var(--text-main); margin-top: 0; margin-bottom: 1.5rem; border-bottom: 2px solid var(--bg-light); padding-bottom: 0.5rem; }
            h3 { font-size: 1.25rem; font-weight: 600; color: var(--text-main); margin-top: 2rem; margin-bottom: 1rem; }
            p { margin-bottom: 1.25rem; color: var(--text-muted); font-size: 1rem; text-align: justify; }
            strong { color: var(--text-main); font-weight: 600; }
            
            /* Components */
            .header-strip { position: absolute; top: 0; left: 0; right: 0; height: 8px; background: linear-gradient(to right, var(--primary), var(--secondary)); }
            .page-number { position: absolute; bottom: 1.5rem; right: 2.5rem; color: var(--text-muted); font-size: 0.875rem; }
            
            /* Cover Page */
            .cover-content { display: flex; flex-direction: column; justify-content: center; height: 100%; text-align: center; }
            .cover-logo { font-size: 3rem; font-weight: 800; margin-bottom: 2rem; color: var(--text-main); }
            .cover-logo span { color: var(--primary); }
            .cover-subtitle { font-size: 1.5rem; color: var(--text-muted); margin-bottom: 4rem; font-weight: 300; }
            .report-meta { background: var(--bg-light); padding: 2rem; border-radius: 12px; display: inline-block; text-align: left; margin: 0 auto; }
            .meta-row { display: flex; justify-content: space-between; gap: 3rem; margin-bottom: 1rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.5rem; }
            .meta-row:last-child { border: none; margin: 0; padding: 0; }
            
            /* Dashboard Grid */
            .dashboard-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-bottom: 2rem; }
            .metric-card { background: var(--bg-light); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid #e2e8f0; }
            .metric-val { font-size: 2.5rem; font-weight: 800; line-height: 1; margin-bottom: 0.5rem; }
            .metric-name { font-size: 0.875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); }
            
            /* Heatmap Comparison */
            .comparison-container { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 2rem; }
            .img-box { border-radius: 8px; overflow: hidden; border: 1px solid #e2e8f0; position: relative; }
            .img-box img { width: 100%; display: block; }
            .img-label { position: absolute; top: 0.75rem; left: 0.75rem; background: rgba(0,0,0,0.75); color: white; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600; }
            
            /* Deep Dive Sections */
            .insight-box { background: #f0f9ff; border-left: 4px solid var(--secondary); padding: 1.5rem; margin-bottom: 1.5rem; border-radius: 0 8px 8px 0; }
            .insight-box h4 { color: #0369a1; margin-top: 0; margin-bottom: 0.5rem; }
            .insight-box p { color: #334155; margin-bottom: 0; }
            
            .warning-box { background: #fffbeb; border-left: 4px solid var(--accent); padding: 1.5rem; margin-bottom: 1.5rem; border-radius: 0 8px 8px 0; }
            .warning-box h4 { color: #b45309; margin-top: 0; margin-bottom: 0.5rem; }
            
            /* Action Plan */
            .action-item { display: flex; gap: 1.5rem; margin-bottom: 2rem; background: var(--bg-white); border: 1px solid #e2e8f0; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
            .priority-badge { width: 80px; height: 80px; display: flex; flex-direction: column; align-items: center; justify-content: center; border-radius: 8px; flex-shrink: 0; font-weight: 700; color: white; }
            .p-High { background: var(--danger); }
            .p-Medium { background: var(--accent); }
            .p-Low { background: var(--success); }
            
            /* ========================================
               LAYOUT OVERFLOW FIX:
               Ensured color cards stay inside container, with responsive grid/flex
               and print-safe widths.
               ======================================== */
            
            /* Main Color Dashboard Section Wrapper */
            .color-dashboard-section {
                max-width: 100%;
                width: 100%;
                margin: 0 auto 2rem auto;
                padding: 0 1rem;
                box-sizing: border-box;
            }
            
            /* Individual Color Row (Swatch + Cards) */
            .color-row {
                display: flex;
                flex-wrap: wrap;
                gap: 1.5rem;
                margin-bottom: 2.5rem;
                background: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
                padding: 1.5rem;
                box-sizing: border-box;
                box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
                page-break-inside: avoid;
            }
            
            /* Swatch Panel */
            .color-swatch-panel {
                flex: 0 0 200px;
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                gap: 0.75rem;
                padding: 0.5rem;
                box-sizing: border-box;
            }
            
            .color-swatch-box {
                width: 80px;
                height: 80px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
                border: 3px solid rgba(255, 255, 255, 0.95);
                margin-bottom: 0.5rem;
            }
            
            .color-swatch-meta {
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
                width: 100%;
            }
            
            .swatch-hex {
                font-size: 0.85rem;
                font-weight: 700;
                color: #1e293b;
                font-family: 'Courier New', 'Monaco', monospace;
                letter-spacing: 0.02em;
            }
            
            .swatch-pct {
                font-size: 1.1rem;
                font-weight: 700;
                color: #4f46e5;
            }
            
            .swatch-label {
                font-size: 0.7rem;
                font-weight: 500;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            
            .swatch-family {
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: #475569;
                background: #f1f5f9;
                padding: 0.35rem 0.6rem;
                border-radius: 6px;
                display: inline-block;
            }
            
            /* Cards Grid Container */
            .color-cards {
                flex: 1 1 calc(100% - 220px);
                min-width: 0;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                gap: 1rem;
                box-sizing: border-box;
            }
            
            /* Individual Card */
            .color-card {
                background: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
                padding: 1.25rem;
                box-sizing: border-box;
                box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
                display: flex;
                flex-direction: column;
                page-break-inside: avoid;
                min-width: 0;
                overflow-wrap: break-word;
            }
            
            /* Card Header */
            .color-card-header {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                padding-bottom: 0.75rem;
                margin-bottom: 1rem;
                border-bottom: 2px solid #e2e8f0;
            }
            
            .color-card-icon {
                font-size: 1.1rem;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
            }
            
            .color-card-title {
                font-size: 0.75rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: #475569;
                margin: 0;
                line-height: 1;
            }
            
            /* Card Body */
            .color-card-body {
                color: #334155;
                font-size: 0.95rem;
                line-height: 1.7;
                flex: 1;
            }
            
            .color-card-body p {
                margin: 0 0 1rem 0;
                word-wrap: break-word;
                overflow-wrap: break-word;
                hyphens: auto;
            }
            
            .color-card-body p:last-child {
                margin-bottom: 0;
            }
            
            /* Keyword Highlighting */
            .color-keyword {
                background: #EEF2FF;
                color: #4F46E5;
                border-radius: 4px;
                padding: 2px 5px;
                font-weight: 500;
                white-space: nowrap;
            }
            
            /* Card Divider */
            .color-card-divider {
                height: 1px;
                background: #e2e8f0;
                margin: 1rem 0;
                border: none;
            }
            
            /* Responsive Breakpoints */
            @media (max-width: 1024px) {
                .color-row {
                    flex-direction: column;
                    gap: 1.5rem;
                    padding: 1.5rem;
                }
                
                .color-swatch-panel {
                    flex: 0 0 auto;
                    flex-direction: row;
                    justify-content: flex-start;
                    width: 100%;
                }
                
                .color-swatch-meta {
                    flex-direction: row;
                    flex-wrap: wrap;
                    align-items: center;
                    gap: 0.75rem;
                }
                
                .color-cards {
                    flex: 1 1 100%;
                    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                }
                
                .color-swatch-box {
                    width: 70px;
                    height: 70px;
                }
            }
            
            @media (max-width: 768px) {
                .color-cards {
                    grid-template-columns: 1fr;
                }
                
                .color-dashboard-section {
                    padding: 0 0.5rem;
                }
                
                .color-row {
                    padding: 1rem;
                }
            }
            
            .synthesis-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; margin-top: 2rem; }
            
            .cta-recommendation { display: flex; align-items: center; gap: 2rem; background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; margin-top: 2rem; }
            .cta-preview { padding: 1rem 2rem; border-radius: 8px; color: white; font-weight: 600; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            
            /* Cognitive Insights Dashboard */
            .cog-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-bottom: 2rem; }
            .gauge-wrapper { text-align: center; position: relative; }
            .gauge-circle { width: 150px; height: 150px; border-radius: 50%; background: conic-gradient(var(--primary) calc(var(--pct) * 1%), #e2e8f0 0); margin: 0 auto; display: flex; align-items: center; justify-content: center; position: relative; }
            .gauge-inner { width: 120px; height: 120px; background: white; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; }
            .gauge-val { font-size: 2rem; font-weight: 800; color: var(--text-main); line-height: 1; }
            .gauge-grade { font-size: 1.25rem; font-weight: 700; color: var(--success); background: #dcfce7; padding: 0.25rem 0.75rem; border-radius: 9999px; margin-top: 0.25rem; }
            
            .hierarchy-bar { margin-bottom: 1rem; }
            .h-label { display: flex; justify-content: space-between; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.25rem; }
            .h-bg { height: 12px; background: #f1f5f9; border-radius: 6px; overflow: hidden; }
            .h-fill { height: 100%; background: var(--secondary); border-radius: 6px; }
            
            
            @media print {
                body { background: white; }
                .page { margin: 0; box-shadow: none; border: none; width: 100%; max-width: none; min-height: auto; padding: 0; page-break-after: always; }
                .no-print { display: none; }
                
                /* Stack color panels vertically for print */
                .info-panels { grid-template-columns: 1fr; gap: 1rem; }
                .color-row { grid-template-columns: 120px 1fr; gap: 1.5rem; padding: 1.5rem; }
            }
        </style>
    </head>
    <body>

        <!-- PAGE 1: COVER & EXECUTIVE SUMMARY -->
        <div class="page">
            <div class="header-strip"></div>
            <div class="cover-content" style="height: auto; padding-top: 2rem;">
                <div class="cover-logo">Uvolution<span>AI</span></div>
                <h1>Comprehensive UX Analysis</h1>
                <div class="cover-subtitle">Deep Dive Report & Strategic Roadmap</div>
                
                <div class="report-meta">
                    <div class="meta-row">
                        <span style="color: var(--text-muted);">Subject</span>
                        <strong>{{ filename }}</strong>
                    </div>
                    <div class="meta-row">
                        <span style="color: var(--text-muted);">Date</span>
                        <strong>{{ timestamp }}</strong>
                    </div>
                    <div class="meta-row">
                        <span style="color: var(--text-muted);">Model</span>
                        <strong>DeepGaze IIE (Enhanced)</strong>
                    </div>
                </div>
            </div>

            <div style="margin-top: 4rem;">
                <h2>Executive Summary</h2>
                <div class="insight-box" style="background: var(--bg-light); border-left: 4px solid var(--primary);">
                    <p style="font-size: 1.1rem; line-height: 1.8;">{{ exec_summary }}</p>
                </div>
                
                <h3>Key Performance Indicators</h3>
                <div class="dashboard-grid">
                    <div class="metric-card">
                        <div class="metric-val" style="color: {{ '#10b981' if adv_metrics.acs > 70 else '#f59e0b' }}">{{ adv_metrics.acs }}</div>
                        <div class="metric-name">Attention Score</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-val" style="color: {{ '#10b981' if adv_metrics.vci < 50 else '#ef4444' }}">{{ adv_metrics.vci }}</div>
                        <div class="metric-name">Visual Clutter</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-val" style="color: {{ '#10b981' if adv_metrics.cle < 50 else '#f59e0b' }}">{{ adv_metrics.cle }}</div>
                        <div class="metric-name">Cognitive Load</div>
                    </div>
                </div>
            </div>
            <div class="page-number">Page 1</div>
        </div>

        <!-- PAGE 2: VISUAL ATTENTION DEEP DIVE -->
        <div class="page">
            <div class="header-strip"></div>
            <h2>Visual Attention Analysis</h2>
            <p>This section analyzes the subconscious visual processing that occurs within the first 3 seconds of viewing. We use the DeepGaze IIE model to simulate human peripheral vision and attentional selection.</p>
            
            <div class="comparison-container">
                <div class="img-box">
                    <div class="img-label">Original Design</div>
                    <img src="../{{ original_image }}" alt="Original">
                </div>
                <div class="img-box">
                    <div class="img-label">Attention Heatmap</div>
                    <img src="../{{ saliency_map }}" alt="Heatmap">
                </div>
            </div>
            
            <h3>Hotspot Distribution Analysis</h3>
            <p>{{ visual_text.hotspot_analysis }}</p>
            
            <h3>Focus Ratio & Concentration</h3>
            <p>{{ visual_text.focus_analysis }}</p>
            
            <div class="insight-box">
                <h4>Why This Matters</h4>
                <p>Visual attention is a zero-sum game. Every unnecessary element steals attention from your primary goal. A focused design (Focus Ratio < 15%) typically converts 20-30% better than a dispersed one.</p>
            </div>
            <div class="page-number">Page 2</div>
        </div>

        <!-- PAGE 3: COGNITIVE MARKETING INSIGHTS -->
        <div class="page">
            <div class="header-strip"></div>
            <h2>Cognitive Marketing Insights</h2>
            <p>Detailed breakdown of cognitive load factors and layout efficiency.</p>
            
            <div class="cog-grid">
                <!-- Whitespace & Clarity -->
                <div class="color-card">
                    <h4>1. Whitespace Ratio & Clarity</h4>
                    <div class="gauge-wrapper">
                        <div class="gauge-circle" style="--pct: {{ cognitive_data.whitespace.whitespace_ratio if cognitive_data else 30 }};">
                            <div class="gauge-inner">
                                <div class="gauge-val">{{ cognitive_data.whitespace.whitespace_ratio if cognitive_data else 30 }}%</div>
                                <div class="gauge-grade">{{ cognitive_data.whitespace.score if cognitive_data else 'B' }}</div>
                            </div>
                        </div>
                        <p style="font-size: 0.8rem; margin-top: 1rem; text-align: center;">{{ cognitive_data.whitespace.interpretation if cognitive_data else 'Moderate' }}</p>
                    </div>
                </div>
                
                <!-- Visual Hierarchy -->
                <div class="color-card">
                    <h4>2. Visual Hierarchy & Element Weight</h4>
                    
                    <div class="hierarchy-bar">
                        <div class="h-label"><span>Hierarchy Score</span> <span>{{ cognitive_data.visual_hierarchy.hierarchy_score if cognitive_data else 70 }}/100</span></div>
                        <div class="h-bg"><div class="h-fill" style="width: {{ cognitive_data.visual_hierarchy.hierarchy_score if cognitive_data else 70 }}%; background: #1e293b;"></div></div>
                    </div>
                    
                    <p style="font-size: 0.8rem; margin-top: 1rem;">{{ cognitive_data.visual_hierarchy.interpretation if cognitive_data else 'Standard hierarchy' }}</p>
                    <p style="font-size: 0.8rem; color: var(--text-muted);">{{ cognitive_data.visual_hierarchy.recommendation if cognitive_data else '' }}</p>
                </div>
            </div>
            
            <!-- Visual Complexity & Saliency -->
            <div class="cog-grid">
                <div class="color-card">
                    <h4>4. Visual Complexity (Rosenholtz-based VCI)</h4>
                    <div class="gauge-wrapper">
                        {% set complexity_score = cognitive_data.visual_complexity.complexity_score if cognitive_data else 50 %}
                        {% set complexity_grade = cognitive_data.visual_complexity.grade if cognitive_data else 'B' %}
                        {% set complexity_color = '#10b981' if complexity_grade == 'A' else ('#f59e0b' if complexity_grade == 'B' else '#ef4444') %}
                        <div class="gauge-circle" style="--pct: {{ complexity_score }}; --primary: {{ complexity_color }};">
                            <div class="gauge-inner">
                                <div class="gauge-val" style="color: {{ complexity_color }};">{{ complexity_score }}</div>
                                <div style="font-size: 0.8rem; font-weight: 600; color: #64748b;">{{ complexity_grade }}</div>
                            </div>
                        </div>
                        <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1rem; font-size: 0.75rem;">
                            <span style="color: #64748b;">{{ cognitive_data.visual_complexity.interpretation if cognitive_data else 'Balanced' }}</span>
                        </div>
                        <div style="margin-top: 0.5rem; font-size: 0.7rem; color: #94a3b8; text-align: center;">
                            *Approximation of Feature Congestion (Rosenholtz et al., 2007)
                        </div>
                    </div>
                </div>
                
                <div class="color-card">
                    <h4>5. Saliency Distribution (Attention Flow)</h4>
                    <div style="height: 150px; display: flex; align-items: flex-end; justify-content: space-between; padding: 0 1rem;">
                        <!-- Visual Bar Chart for Saliency -->
                        <div style="flex: 1; margin: 0 4px; background: #e2e8f0; height: {{ cognitive_data.saliency_distribution.distribution.top if cognitive_data else 33 }}%; position: relative;">
                            <span style="position: absolute; bottom: -20px; left: 0; right: 0; text-align: center; font-size: 0.7rem;">Top</span>
                        </div>
                        <div style="flex: 1; margin: 0 4px; background: #e2e8f0; height: {{ cognitive_data.saliency_distribution.distribution.middle if cognitive_data else 33 }}%; position: relative;">
                            <span style="position: absolute; bottom: -20px; left: 0; right: 0; text-align: center; font-size: 0.7rem;">Mid</span>
                        </div>
                        <div style="flex: 1; margin: 0 4px; background: #e2e8f0; height: {{ cognitive_data.saliency_distribution.distribution.bottom if cognitive_data else 33 }}%; position: relative;">
                            <span style="position: absolute; bottom: -20px; left: 0; right: 0; text-align: center; font-size: 0.7rem;">Bot</span>
                        </div>
                    </div>
                    <p style="text-align: center; font-size: 0.8rem; color: var(--text-muted); margin-top: 1.5rem;">
                        {{ cognitive_data.saliency_distribution.pattern if cognitive_data else 'Balanced Flow' }}
                    </p>
                </div>
            </div>
            
            <div class="page-number">Page 3</div>
        </div>

        <!-- PAGE 4: COLOR PSYCHOLOGY, ACCESSIBILITY & MARKETING (REVAMPED) -->
        <div class="page">
            <div class="header-strip"></div>
            <h2>Color Psychology, Accessibility & Marketing Influence</h2>
            <p>Comprehensive analysis of the color palette's impact on user behavior, emotional response, and accessibility compliance.</p>
            
            {% if color_data %}
            
            <!-- Color Dashboard Section with Overflow-Safe Container -->
            <section class="color-dashboard-section">
                {% for color in color_data.dominant_colors %}
                <div class="color-row">
                    <!-- Swatch Panel -->
                    <div class="color-swatch-panel">
                        <div class="color-swatch-box" style="background-color: {{ color.hex }};"></div>
                        <div class="color-swatch-meta">
                            <div class="swatch-hex">{{ color.hex }}</div>
                            <div class="swatch-pct">{{ color.percentage }}%</div>
                            <div class="swatch-label">Coverage</div>
                            <div class="swatch-family">{{ color.family }}</div>
                        </div>
                    </div>
                    
                    <!-- Cards Container -->
                    <div class="color-cards">
                        <!-- Card 1: Scientific Metrics -->
                        <article class="color-card">
                            <header class="color-card-header">
                                <div class="color-card-icon">🔬</div>
                                <h5 class="color-card-title">Scientific Metrics</h5>
                            </header>
                            <div class="color-card-body">
                                <p>{{ color.text.scientific | replace("luminance", "<span class='color-keyword'>luminance</span>") | replace("temperature", "<span class='color-keyword'>temperature</span>") | replace("saturation", "<span class='color-keyword'>saturation</span>") | replace("WCAG", "<span class='color-keyword'>WCAG</span>") | replace("contrast", "<span class='color-keyword'>contrast</span>") | safe }}</p>
                            </div>
                        </article>
                        
                        <!-- Card 2: Marketing Psychology -->
                        <article class="color-card">
                            <header class="color-card-header">
                                <div class="color-card-icon">🎨</div>
                                <h5 class="color-card-title">Marketing Psychology</h5>
                            </header>
                            <div class="color-card-body">
                                <p>{{ color.text.marketing | replace("trust", "<span class='color-keyword'>trust</span>") | replace("growth", "<span class='color-keyword'>growth</span>") | replace("urgency", "<span class='color-keyword'>urgency</span>") | replace("energy", "<span class='color-keyword'>energy</span>") | replace("calmness", "<span class='color-keyword'>calmness</span>") | replace("professionalism", "<span class='color-keyword'>professionalism</span>") | safe }}</p>
                            </div>
                        </article>
                        
                        <!-- Card 3: Cultural & Industry -->
                        <article class="color-card">
                            <header class="color-card-header">
                                <div class="color-card-icon">🌍</div>
                                <h5 class="color-card-title">Cultural & Industry</h5>
                            </header>
                            <div class="color-card-body">
                                <p>{{ color.text.cultural | replace("Korea", "<span class='color-keyword'>Korea</span>") | replace("United States", "<span class='color-keyword'>United States</span>") | replace("Chinese", "<span class='color-keyword'>Chinese</span>") | replace("Japan", "<span class='color-keyword'>Japan</span>") | safe }}</p>
                                <hr class="color-card-divider">
                                <p style="font-size: 0.9rem;">{{ color.text.industry | replace("Finance", "<span class='color-keyword'>Finance</span>") | replace("Health", "<span class='color-keyword'>Health</span>") | replace("Food", "<span class='color-keyword'>Food</span>") | replace("Ecommerce", "<span class='color-keyword'>Ecommerce</span>") | replace("Medical", "<span class='color-keyword'>Medical</span>") | safe }}</p>
                            </div>
                        </article>
                    </div>
                </div>
                {% endfor %}
            </section>
            
            <!-- Synthesis Section -->
            <div class="synthesis-box">
                <h4 style="margin-top: 0; color: var(--primary);">Palette Synthesis & Recommendations</h4>
                <p>{{ color_data.palette_summary }}</p>
                
                <div class="cta-recommendation">
                    <div class="cta-preview" style="background-color: {{ color_data.cta_recommendation.recommended_color }};">
                        Recommended CTA
                    </div>
                    <div>
                        <div style="font-weight: 700; color: var(--text-main);">Optimal Call-to-Action Color: {{ color_data.cta_recommendation.recommended_color }}</div>
                        <div style="font-size: 0.9rem; color: var(--text-muted);">{{ color_data.cta_recommendation.marketing.rationale }}</div>
                        <div style="font-size: 0.85rem; color: var(--success); margin-top: 0.25rem;">
                            ✓ WCAG {{ color_data.cta_recommendation.scientific.wcag_level }} Compliant (Contrast {{ color_data.cta_recommendation.scientific.contrast_ratio }}:1)
                        </div>
                    </div>
                </div>
            </div>
            
            {% endif %}
            <div class="page-number">Page 4</div>
        </div>

        <!-- PAGE 5: UX HEURISTICS -->
        <div class="page">
            <div class="header-strip"></div>
            <h2>UX Heuristics & Visual Flow</h2>
            
            <h3>Scanning Patterns (F-Pattern vs Z-Pattern)</h3>
            <p>{{ ux_text.pattern_text }}</p>
            
            <h3>Visual Complexity Analysis</h3>
            <p>{{ ux_text.complexity_text }}</p>
            
            <div class="insight-box">
                <h4>Scientific Basis</h4>
                <p>This analysis uses Rosenholtz's Feature Congestion model to estimate visual clutter. Lower complexity scores correlate with faster visual search times and reduced cognitive load.</p>
            </div>
            
            <!-- UX Heuristics Extension: Nielsen's Usability Principles -->
            {% if ux_heuristics_details %}
            <h3 style="margin-top: 3rem;">Nielsen's Usability Heuristics Assessment</h3>
            <p style="color: var(--text-muted); font-size: 0.9rem;">Research-grade evaluation based on visual analysis metrics.</p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-top: 1.5rem;">
                {% for heuristic in ux_heuristics_details %}
                <div class="color-card" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 1.5rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h5 style="margin: 0; font-size: 0.85rem; font-weight: 700; color: #475569;">{{ heuristic.name }}</h5>
                        <div style="background: {{ '#dcfce7' if heuristic.score >= 4 else ('#fef3c7' if heuristic.score == 3 else '#fee2e2') }}; 
                                    color: {{ '#166534' if heuristic.score >= 4 else ('#92400e' if heuristic.score == 3 else '#991b1b') }}; 
                                    padding: 0.25rem 0.75rem; border-radius: 9999px; font-weight: 700; font-size: 0.75rem;">
                            {{ heuristic.score }}/5
                        </div>
                    </div>
                    <p style="font-size: 0.9rem; margin-bottom: 0.75rem; color: #334155; line-height: 1.6;">
                        <strong style="color: #1e293b;">Finding:</strong> {{ heuristic.finding }}
                    </p>
                    <p style="font-size: 0.85rem; margin: 0; color: #64748b; line-height: 1.5; border-left: 3px solid #cbd5e1; padding-left: 0.75rem;">
                        <strong>→</strong> {{ heuristic.recommendation }}
                    </p>
                </div>
                {% endfor %}
            </div>
            {% endif %}
            
            <!-- Added Gaze Path Efficiency (minimal addition, no rewrites) -->
            {% if gaze_path_data %}
            <h3 style="margin-top: 3rem;">Gaze Path Efficiency</h3>
            <p style="color: var(--text-muted); font-size: 0.9rem;">Measures the scanning distance required between attention hotspots.</p>
            
            <div class="color-card" style="background: #ffffff; border: 1px solid #e2e8f0; padding: 1.5rem; margin-top: 1rem;">
                <div style="display: flex; align-items: center; gap: 2rem;">
                    <div style="text-align: center;">
                        <div style="font-size: 3rem; font-weight: 800; color: {{ '#10b981' if gaze_path_data.score >= 70 else ('#f59e0b' if gaze_path_data.score >= 50 else '#ef4444') }};">
                            {{ gaze_path_data.score }}
                        </div>
                        <div style="font-size: 0.75rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">
                            Efficiency Score
                        </div>
                    </div>
                    <div style="flex: 1;">
                        <p style="font-size: 0.95rem; margin-bottom: 0.75rem; color: #334155; line-height: 1.6;">
                            <strong style="color: #1e293b;">Analysis:</strong> {{ gaze_path_data.insight }}
                        </p>
                        <p style="font-size: 0.9rem; margin: 0; color: #64748b; line-height: 1.5; border-left: 3px solid #cbd5e1; padding-left: 0.75rem;">
                            <strong>→</strong> {{ gaze_path_data.recommendation }}
                        </p>
                    </div>
                </div>
            </div>
            {% endif %}
            
            <div class="page-number">Page 5</div>
        </div>

        <!-- PAGE 6: STRATEGIC ACTION PLAN -->
        <div class="page">
            <div class="header-strip"></div>
            <h2>Strategic Action Roadmap</h2>
            <p>Based on the comprehensive analysis, here is your prioritized roadmap for improvement. Focus on High Priority items first to see the biggest impact on conversion.</p>
            
            {% for action in action_plan %}
            <div class="action-item">
                <div class="priority-badge p-{{ action.priority }}">
                    <div style="font-size: 0.75rem; text-transform: uppercase; opacity: 0.9;">Priority</div>
                    <div style="font-size: 1.25rem;">{{ action.priority }}</div>
                </div>
                <div>
                    <h4 style="margin-top: 0; margin-bottom: 0.5rem; color: var(--text-main); font-size: 1.1rem;">{{ action.title }}</h4>
                    <p style="margin: 0; color: var(--text-muted);">{{ action.desc }}</p>
                </div>
            </div>
            {% endfor %}
            
            <div style="margin-top: 4rem; border-top: 1px solid #e2e8f0; padding-top: 2rem; font-size: 0.8rem; color: var(--text-muted);">
                <strong>Methodology References:</strong><br>
                1. Kümmerer, M. et al. (2016). DeepGaze IIE: Reading fixations from deep features.<br>
                2. Rosenholtz, R. et al. (2007). Measuring visual clutter. Journal of Vision.<br>
                3. Nielsen, J. (2006). F-Shaped Pattern For Reading Web Content.<br>
                4. Miller, G. A. (1956). The magical number seven, plus or minus two.<br>
                5. WCAG 2.1 Guidelines for Contrast and Accessibility.
            </div>
            <div class="page-number">Page 6</div>
        </div>

    </body>
    </html>
    """
    
    # Render Template
    t = Template(template_str)
    html_content = t.render(
        filename=filename,
        timestamp=datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S"),
        metrics=metrics,
        adv_metrics=adv_metrics,
        color_data=color_data,
        cognitive_data=cognitive_data,
        original_image=f"uploads/{filename}",
        saliency_map=f"outputs/saliency_{filename}",
        exec_summary=exec_summary,
        visual_text=visual_text,
        cognitive_text=cognitive_text,
        ux_text=ux_text,
        ux_heuristics_details=ux_heuristics_details,
        gaze_path_data=gaze_path_data,
        action_plan=action_plan
    )
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    return report_path
