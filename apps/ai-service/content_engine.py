"""
Content Engine for Uvolution AI Reports.
Generates expert-level, context-aware text for UX analysis reports.
Strictly adheres to visually verifiable data.

# Color Report Revamp:
# Increased detail, added scientific metrics, cultural variants, 
# industry-specific insights, improved layout, stronger UX narrative.
"""

def get_executive_summary_text(acs, cle, hotspot_count):
    """Generates the executive summary text based on high-level metrics."""
    
    # Attention Capture Assessment
    if acs >= 75:
        attn_text = "The design exhibits <strong>exceptional attention-capturing capabilities</strong>. The primary visual anchors are highly salient, effectively directing the user's gaze immediately upon page load. This configuration is optimal for high-impact landing pages or promotional assets where immediate engagement is the primary KPI."
    elif acs >= 50:
        attn_text = "The design demonstrates <strong>moderate attention capture</strong>. While key elements are discernible, they do not aggressively compete for the user's foveal vision. This approach is often suitable for content-dense interfaces where a balanced visual hierarchy is preferred over singular focus."
    else:
        attn_text = "The design currently presents <strong>low attention capture potential</strong>. The visual hierarchy appears subtle, which may result in users overlooking critical entry points. For conversion-centric pages, this indicates a strategic need to amplify the visual weight of primary Calls-to-Action (CTAs)."

    # Cognitive Load Assessment
    if cle < 40:
        cog_text = "Crucially, the <strong>cognitive friction is minimized</strong>, suggesting users can process the information architecture with near-zero latency. This synergy of high attention and low load typically correlates with maximal task completion rates."
    elif cle < 65:
        cog_text = "The <strong>cognitive load is optimized</strong>, requiring a standard level of mental processing. This aligns with industry benchmarks for modern web interfaces, though targeted simplification of complex modules could further enhance the user journey."
    else:
        cog_text = "However, the <strong>cognitive load is elevated</strong>. Users may experience 'information overload' or visual clutter, which significantly increases the risk of decision paralysis and bounce rates."

    return f"{attn_text} {cog_text}"

def get_visual_attention_deep_dive(hotspot_count, focus_ratio):
    """Generates deep dive text for the Visual Attention section."""
    
    # Hotspot Analysis
    if hotspot_count <= 2:
        hotspot_analysis = f"Our analysis detected only <strong>{hotspot_count} primary visual anchors</strong>. This indicates a highly singular focus. While this minimizes distraction, it risks 'banner blindness' if the solitary focal point does not align with the user's immediate intent."
    elif hotspot_count <= 5:
        hotspot_analysis = f"We detected <strong>{hotspot_count} distinct attention hotspots</strong>, which falls within the optimal range (3-5) for human working memory. This suggests a robust visual hierarchy where users can intuitively navigate between key information clusters."
    else:
        hotspot_analysis = f"The analysis reveals <strong>{hotspot_count} competing attention hotspots</strong>. This exceeds the optimal processing capacity (Miller's Law, 7±2). Users are likely to engage in chaotic scanning rather than following a linear, persuasive narrative."

    # Focus Ratio Analysis
    if focus_ratio < 15:
        focus_analysis = "The <strong>Focus Ratio is highly concentrated (<15%)</strong>, meaning attention is funneled to specific coordinates. This is exemplary for <strong>conversion funnels</strong> where the objective is to drive users toward a singular action."
    elif focus_ratio < 30:
        focus_analysis = "The <strong>Focus Ratio is balanced (15-30%)</strong>, indicating a healthy distribution of attention. This is typical for <strong>informational dashboards</strong> where users must scan multiple data points simultaneously."
    else:
        focus_analysis = "The <strong>Focus Ratio is dispersed (>30%)</strong>, suggesting attention is diluted across the viewport. This pattern is often observed in <strong>cluttered interfaces</strong> or text-heavy pages lacking clear visual anchors."

    return {
        "hotspot_analysis": hotspot_analysis,
        "focus_analysis": focus_analysis
    }

def get_cognitive_load_deep_dive(vci, whitespace_ratio):
    """Generates deep dive text for the Cognitive Load section."""
    
    # VCI Analysis
    if vci < 40:
        vci_text = "The <strong>Visual Clutter Index (VCI) is exceptionally low</strong>, indicating a pristine, minimalist aesthetic. This significantly reduces the 'interaction cost' for users, facilitating rapid information retrieval and decision-making."
    elif vci < 60:
        vci_text = "The <strong>Visual Clutter Index (VCI) is moderate</strong>. The design maintains sufficient visual fidelity to be engaging without introducing chaotic noise. This represents a strategic 'sweet spot' for most corporate and e-commerce applications."
    else:
        vci_text = "The <strong>Visual Clutter Index (VCI) is critical</strong>. High edge density and chromatic variance are generating substantial visual noise. This forces the user's cognitive faculties to expend unnecessary effort filtering irrelevant signals."

    # Whitespace Analysis
    if whitespace_ratio > 50:
        ws_text = "The layout utilizes <strong>ample whitespace (>50%)</strong>. This 'negative space' is not merely empty; it serves as an active design element that logically groups content and enhances readability through proximity."
    elif whitespace_ratio > 30:
        ws_text = "The <strong>whitespace ratio is balanced (30-50%)</strong>. Content density is optimized to be informative yet legible. Ensure that margins between distinct semantic sections are consistent to maintain rhythm."
    else:
        ws_text = "The <strong>whitespace ratio is constrained (<30%)</strong>. The interface appears dense. Lack of 'breathing room' compromises scannability and makes element differentiation cognitively taxing."

    return {
        "vci_text": vci_text,
        "whitespace_text": ws_text
    }

def get_ux_heuristics_text(complexity_data, hotspot_count):
    """Generates text for UX Heuristics section."""
    
    # F-Pattern / Z-Pattern
    if hotspot_count <= 5:
        pattern_text = "The arrangement of focal points supports a clear <strong>Z-Pattern scanning path</strong>. Users typically initiate scanning at the top-left (Primary Anchor), traverse horizontally (Navigation/Action), and then diagonally descend to the core content or CTA."
    else:
        pattern_text = "The high frequency of focal points suggests users may default to an <strong>F-Pattern scanning mode</strong>, typical of text-heavy or cluttered interfaces. They will likely scan the top header heavily but then vertically skim the left axis, ignoring content on the right periphery."

    # Visual Complexity (Replacing Mobile Speed)
    if complexity_data['grade'] == 'A':
        complexity_text = "The design maintains <strong>minimal visual complexity</strong>, which correlates with accelerated cognitive processing. Users can instantaneously identify the page's utility without visual friction."
    elif complexity_data['grade'] == 'B':
        complexity_text = "The design shows <strong>balanced visual complexity</strong>. It provides sufficient detail to be informative without being perceptually overwhelming. This is a standard pattern for effective, high-usability interfaces."
    else:
        complexity_text = "The design exhibits <strong>high visual complexity</strong>. Research (Rosenholtz et al.) indicates this increases the 'time-to-target' for finding specific information and significantly correlates with higher abandonment rates."

    return {
        "pattern_text": pattern_text,
        "complexity_text": complexity_text
    }

# UX Heuristics Extension:
# Added richer, research-oriented heuristic analysis
# using incremental changes without rewriting core files.

def build_ux_heuristics_details(metrics, adv_metrics, cognitive_data, color_data):
    """
    Extends UX heuristics with Nielsen's principles and modern UX research.
    Returns structured heuristic insights based on existing metrics.
    Designed to supplement (not replace) get_ux_heuristics_text.
    """
    heuristics = []
    
    # 1. Visibility of System Status
    # Assessed via attention capture and hotspot clarity
    acs = adv_metrics.get('acs', 50)
    if acs > 70:
        heuristics.append({
            "name": "Visibility of System Status",
            "score": 5,
            "finding": "Strong visual anchors provide immediate system feedback.",
            "recommendation": "Maintain current emphasis on primary status indicators."
        })
    elif acs < 40:
        heuristics.append({
            "name": "Visibility of System Status",
            "score": 2,
            "finding": "Low attention capture may obscure critical system state indicators.",
            "recommendation": "Amplify contrast and scale of primary status elements."
        })
    else:
        heuristics.append({
            "name": "Visibility of System Status",
            "score": 3,
            "finding": "Moderate attention capture provides adequate but not optimal feedback.",
            "recommendation": "Enhance visibility of primary action states."
        })
    
    # 2. Consistency and Standards
    # Assessed via color palette consistency
    if color_data and len(color_data.get('dominant_colors', [])) > 5:
        heuristics.append({
            "name": "Consistency & Standards",
            "score": 2,
            "finding": f"{len(color_data['dominant_colors'])} dominant colors detected, suggesting potential style fragmentation.",
            "recommendation": "Consolidate palette to 3-4 primary hues to enforce visual coherence."
        })
    elif color_data and len(color_data.get('dominant_colors', [])) <= 3:
        heuristics.append({
            "name": "Consistency & Standards",
            "score": 5,
            "finding": "Restricted color palette demonstrates strong adherence to design system standards.",
            "recommendation": "Excellent discipline. Maintain current chromatic consistency."
        })
    
    # 3. Aesthetic and Minimalist Design
    # Assessed via visual complexity and cognitive load
    vci = adv_metrics.get('vci', 50)
    cle = adv_metrics.get('cle', 50)
    
    if vci < 40 and cle < 40:
        heuristics.append({
            "name": "Aesthetic & Minimalist Design",
            "score": 5,
            "finding": "Minimalist aesthetic significantly reduces cognitive friction.",
            "recommendation": "Exemplary. Preserve current signal-to-noise ratio."
        })
    elif vci > 60 or cle > 65:
        heuristics.append({
            "name": "Aesthetic & Minimalist Design",
            "score": 2,
            "finding": "High visual complexity is taxing user cognitive resources.",
            "recommendation": "Eliminate non-functional decorative elements. Increase negative space by >30%."
        })
    else:
        heuristics.append({
            "name": "Aesthetic & Minimalist Design",
            "score": 3,
            "finding": "Moderate complexity balances information density with clarity.",
            "recommendation": "Audit and remove lowest-priority visual artifacts."
        })
    
    # 4. Recognition Rather Than Recall
    # Assessed via focus ratio and information density
    focus_ratio = metrics.get('focus_ratio', 20)
    if focus_ratio < 15:
        heuristics.append({
            "name": "Recognition Rather Than Recall",
            "score": 5,
            "finding": "Tight visual focus minimizes working memory load.",
            "recommendation": "Optimal. Key affordances are immediately perceptible."
        })
    elif focus_ratio > 35:
        heuristics.append({
            "name": "Recognition Rather Than Recall",
            "score": 2,
            "finding": "Dispersed attention forces users to rely on spatial memory.",
            "recommendation": "Establish stronger visual anchors for primary user flows."
        })
    
    # 5. Flexibility and Efficiency
    # Assessed via hotspot distribution
    hotspot_count = metrics.get('hotspot_count', 3)
    if 3 <= hotspot_count <= 5:
        heuristics.append({
            "name": "Flexibility & Efficiency",
            "score": 4,
            "finding": "Optimal hotspot count (3-5) facilitates efficient scanning for both novice and expert users.",
            "recommendation": "Well-balanced. Ensure accelerators are discoverable."
        })
    elif hotspot_count > 7:
        heuristics.append({
            "name": "Flexibility & Efficiency",
            "score": 2,
            "finding": "Excessive focal points impede rapid scanning by expert users.",
            "recommendation": "Implement progressive disclosure to hide secondary features."
        })
    
    # 6. Error Prevention (Accessibility)
    # Assessed via color contrast issues
    if color_data and color_data.get('contrast_issues'):
        issue_count = len(color_data['contrast_issues'])
        heuristics.append({
            "name": "Error Prevention (Accessibility)",
            "score": 1,
            "finding": f"{issue_count} contrast violations detected. High risk of readability errors.",
            "recommendation": "Remediate WCAG AA failures immediately to ensure inclusive access."
        })
    elif color_data:
        heuristics.append({
            "name": "Error Prevention (Accessibility)",
            "score": 5,
            "finding": "All color pairings meet or exceed accessibility contrast standards.",
            "recommendation": "Excellent. Maintain strict contrast compliance in future updates."
        })
    
    # 7. Help Users Recognize, Diagnose, and Recover from Errors
    # Generic best practice reminder
    heuristics.append({
        "name": "Error Recovery",
        "score": 3,
        "finding": "Static analysis limit. Verify error state visibility.",
        "recommendation": "Ensure error messaging is explicit, precise, and constructive."
    })
    
    return heuristics


# Added Gaze Path Efficiency (minimal addition, no rewrites)

def build_gaze_path_efficiency(saliency_map_path):
    """
    Computes gaze path efficiency based on hotspot distribution.
    Uses existing saliency map to calculate sequential scanning distance.
    Returns efficiency score (0-100) where higher = more efficient scanning path.
    """
    import cv2
    import numpy as np
    
    try:
        saliency = cv2.imread(saliency_map_path, cv2.IMREAD_GRAYSCALE)
        if saliency is None:
            return {"score": 50, "insight": "Unable to compute gaze path.", "recommendation": "N/A"}
        
        total_area = saliency.size
        
        # Extract hotspots using same logic as calculate_metrics
        _, thresh = cv2.threshold(saliency, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        hotspots = [c for c in contours if cv2.contourArea(c) > (total_area * 0.001)]
        
        if len(hotspots) < 2:
            return {
                "score": 90,
                "insight": "Single focal point creates direct, efficient scanning path.",
                "recommendation": "Excellent for conversion-focused pages."
            }
        
        # Compute centroids of hotspots
        centroids = []
        for contour in hotspots:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                centroids.append((cx, cy))
        
        if len(centroids) < 2:
            return {"score": 85, "insight": "Minimal gaze path required.", "recommendation": "Good focus."}
        
        # Sort centroids by typical reading pattern (top-to-bottom, left-to-right)
        centroids_sorted = sorted(centroids, key=lambda p: (p[1], p[0]))
        
        # Calculate total path distance
        total_distance = 0
        for i in range(len(centroids_sorted) - 1):
            x1, y1 = centroids_sorted[i]
            x2, y2 = centroids_sorted[i + 1]
            distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            total_distance += distance
        
        # Normalize by image diagonal (max possible distance)
        h, w = saliency.shape
        diagonal = np.sqrt(h**2 + w**2)
        
        # Average distance between hotspots as percentage of diagonal
        avg_distance = total_distance / (len(centroids_sorted) - 1)
        distance_ratio = avg_distance / diagonal
        
        # Convert to efficiency score (shorter distances = higher efficiency)
        # Typical good value: 0.2-0.4 of diagonal
        if distance_ratio < 0.25:
            score = 90
            insight = "Hotspots are tightly clustered, minimizing eye travel distance."
            recommendation = "Excellent scanning efficiency. Maintain current layout."
        elif distance_ratio < 0.5:
            score = 70
            insight = "Moderate gaze path length. Users scan naturally between focal points."
            recommendation = "Good. Consider grouping related elements closer if possible."
        else:
            score = 40
            distance_percent = int(distance_ratio * 100)
            insight = f"Hotspots are widely dispersed ({distance_percent}% of screen diagonal). High eye travel required."
            recommendation = "Reduce scanning fatigue: group related CTAs within closer proximity."
        
        return {
            "score": score,
            "insight": insight,
            "recommendation": recommendation
        }
        
    except Exception as e:
        return {
            "score": 50,
            "insight": f"Gaze path analysis unavailable: {str(e)}",
            "recommendation": "Manual review recommended."
        }


def get_strategic_action_plan(metrics, adv_metrics, cognitive_data):
    """Generates the prioritized Strategic Action Plan."""
    
    actions = []
    
    # Priority 1: Critical Fixes (Red flags)
    if adv_metrics['vci'] > 60:
        actions.append({
            "priority": "High",
            "title": "De-clutter the Interface",
            "desc": "The Visual Clutter Index exceeds optimal thresholds. <strong>Action:</strong> Reduce non-essential decorative elements (icons, borders, patterns) by at least 20%. Increase negative space between semantic sections to reduce cognitive friction."
        })
    
    if metrics['hotspot_count'] > 6:
        actions.append({
            "priority": "High",
            "title": "Consolidate Attention Points",
            "desc": f"There are {metrics['hotspot_count']} competing focal points, diluting user attention. <strong>Action:</strong> Designate ONE primary conversion goal. Visually demote secondary elements by reducing scale, contrast, or saturation."
        })

    # Priority 2: Optimization (Yellow flags)
    if cognitive_data and cognitive_data['cta_placement']['recommendations']:
        rec = cognitive_data['cta_placement']['recommendations'][0]
        if "✓" not in rec:
            actions.append({
                "priority": "Medium",
                "title": "Optimize Call-to-Action (CTA)",
                "desc": f"<strong>Action:</strong> {rec} Ensure the CTA utilizes a color that achieves a high contrast ratio against its immediate container."
            })
        
    if metrics['focus_ratio'] > 30:
         actions.append({
            "priority": "Medium",
            "title": "Strengthen Visual Hierarchy",
            "desc": "Attention is widely dispersed. <strong>Action:</strong> Amplify scale contrast. Increase H1 headline size (2.5x body text) and establish the Hero Image as the dominant visual anchor."
        })

    # Priority 3: Refinement (Green flags/General advice)
    actions.append({
        "priority": "Low",
        "title": "Enhance Accessibility",
        "desc": "<strong>Action:</strong> Audit all text elements for WCAG AA compliance (4.5:1 contrast). Implement descriptive alt text for all semantic imagery."
    })
    
    actions.append({
        "priority": "Low",
        "title": "Visual Balance Check",
        "desc": "<strong>Action:</strong> Verify whitespace distribution. Eliminate 'trapped whitespace' (voids surrounded by content) which can create inadvertent focal points."
    })

    return actions

def get_emotion_icon(emotion):
    """Maps emotions to FontAwesome-style icon names (or unicode characters)."""
    icons = {
        "trust": "🤝",
        "reliability": "🛡️",
        "security": "🔒",
        "urgency": "⚡",
        "energy": "🔥",
        "excitement": "🎉",
        "growth": "📈",
        "eco-friendly": "🌿",
        "optimism": "😊",
        "happiness": "☀️",
        "luxury": "💎",
        "creativity": "🎨",
        "sophistication": "🎩",
        "power": "💪",
        "purity": "🕊️",
        "cleanliness": "✨",
        "danger": "⚠️",
        "passion": "❤️",
        "confidence": "🦁",
        "friendliness": "👋",
        "warmth": "☕",
        "enthusiasm": "🤩",
        "attention": "🔔",
        "caution": "🚧",
        "balance": "⚖️",
        "logic": "🧠",
        "wisdom": "🦉",
        "spirituality": "🧘",
        "mystery": "🕵️",
        "elegance": "👠",
        "authority": "👑",
        "simplicity": "⚪",
        "clarity": "👓"
    }
    return icons.get(emotion.lower(), "✨")

def calculate_contrast_score(current_contrast, recommended_contrast):
    """
    Calculates a 'Contrast Score' improvement metric.
    Replaces speculative CTR prediction with verifiable contrast math.
    """
    # Normalize contrast to a 0-100 score (21:1 is max, 1:1 is min)
    # WCAG AAA is 7:1, AA is 4.5:1
    
    def contrast_to_score(c):
        if c >= 7.0: return 100
        if c >= 4.5: return 80 + ((c-4.5)/(7.0-4.5))*20
        if c >= 3.0: return 50 + ((c-3.0)/(4.5-3.0))*30
        return max(0, (c-1.0)/2.0 * 50)
        
    current_score = contrast_to_score(current_contrast)
    target_score = contrast_to_score(recommended_contrast)
    
    improvement = target_score - current_score
    
    return {
        "current_score": round(current_score),
        "target_score": round(target_score),
        "improvement": round(improvement)
    }

# --- NEW COLOR REPORT GENERATORS ---

# Whitespace Normalization:
# Fix inconsistent spacing, remove double spaces,
# clean punctuation spacing, and standardize readability.

import re

def normalize_whitespace(text):
    """
    Normalizes all whitespace in text:
    - Collapses multiple spaces to single space
    - Removes non-breaking spaces and HTML entities
    - Fixes punctuation spacing (no space before comma/period/colon)
    - Trims leading/trailing whitespace
    - Removes random line breaks inside sentences
    """
    if not text:
        return text
    
    # Replace non-breaking spaces and HTML entities
    text = text.replace('\u00a0', ' ')  # Non-breaking space
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    
    # Collapse multiple spaces into single space
    text = re.sub(r' {2,}', ' ', text)
    
    # Fix space before punctuation
    text = re.sub(r'\s+([,.:;!?])', r'\1', text)
    
    # Ensure space after punctuation (except at end of string)
    text = re.sub(r'([,.:;])([^\s\d])', r'\1 \2', text)
    
    # Remove random line breaks inside sentences (but keep intentional paragraph breaks)
    text = re.sub(r'([a-z,])\s*\n\s*([a-z])', r'\1 \2', text, flags=re.IGNORECASE)
    
    # Trim leading and trailing whitespace
    text = text.strip()
    
    # Remove spaces at start/end of lines
    text = '\n'.join(line.strip() for line in text.split('\n'))
    
    return text

# Color Report Concise Mode:
# Rewriting long descriptive paragraphs into concise, actionable,
# marketing-research-style insights.

def generate_color_scientific_text(color_data):
    """Generates concise scientific assessment text."""
    sci = color_data.get('scientific', {})
    if not sci: return "No scientific data available."
    
    lum = sci.get('luminance', 0)
    temp = sci.get('temperature', 'Neutral')
    hsv = sci.get('hsv', {})
    sat = hsv.get('saturation', 0)
    
    # Build concise insights
    parts = []
    
    # Luminance
    if lum > 0.8:
        parts.append(f"High luminance ({lum}) creates openness but requires dark text for contrast.")
    elif lum < 0.2:
        parts.append(f"Low luminance ({lum}) gives strong visual weight, requires light text for accessibility.")
    else:
        parts.append(f"Mid-range luminance ({lum}) offers flexible text pairing options.")
    
    # Temperature
    if "Warm" in temp:
        parts.append(f"{temp} temperature advances visually, creating energy and proximity.")
    elif "Cool" in temp:
        parts.append(f"{temp} temperature recedes, signaling calm and professionalism.")
    else:
        parts.append(f"{temp} temperature provides balanced neutrality.")
    
    # Saturation
    if sat > 80:
        parts.append(f"High saturation ({sat}%) grabs attention instantly—best for accents to avoid fatigue.")
    elif sat < 20:
        parts.append(f"Low saturation ({sat}%) conveys sophistication and restraint, ideal for corporate use.")
    else:
        parts.append(f"Moderate saturation ({sat}%) balances visibility with comfort.")
    
    return normalize_whitespace(" ".join(parts))

def generate_color_marketing_text(color_data):
    """Generates concise marketing psychology text."""
    mkt = color_data.get('marketing', {})
    if not mkt: return "No marketing data available."
    
    fam = mkt.get('color_family', 'Unknown').title()
    emotions = mkt.get('emotions', [])
    psych = mkt.get('psychology', '')
    
    # Build concise narrative
    parts = []
    
    if emotions:
        emotion_list = ', '.join(emotions[:3])
        parts.append(f"{fam} signals {emotion_list}.")
    
    # Add specific application insight
    if fam == "Blue":
        parts.append("Reduces anxiety, dominates corporate/fintech for trust-building.")
    elif fam == "Red":
        parts.append("Creates urgency, drives action—effective for sales and clearance CTAs.")
    elif fam == "Green":
        parts.append("Reduces cognitive load, signals 'proceed'—strong for confirmations and health messaging.")
    elif fam == "Orange":
        parts.append("Combines energy with approachability—effective for non-threatening CTAs.")
    elif fam == "Yellow":
        parts.append("Maximizes visibility but use sparingly to prevent eye strain.")
    elif fam == "Purple":
        parts.append("Signals luxury and quality, effective for premium positioning.")
    else:
        parts.append(f"{psych.split('.')[0] if psych else 'Context-dependent application'}.")
    
    return normalize_whitespace(" ".join(parts))

def generate_color_cultural_text(color_data):
    """Generates concise cultural context text."""
    mkt = color_data.get('marketing', {})
    variants = mkt.get('cultural_variants', {})
    
    if not variants: return "No cultural variance data available."
    
    # Build concise regional insights
    regional = []
    if 'kr' in variants:
        regional.append(f"KR: {variants['kr']}")
    if 'us' in variants:
        regional.append(f"US: {variants['us']}")
    if 'cn' in variants:
        regional.append(f"CN: {variants['cn']}")
    if 'jp' in variants:
        regional.append(f"JP: {variants['jp']}")
    
    text = "Cultural variance: " + "; ".join(regional[:3]) + "."
    if len(regional) > 3:
        text += f" ({len(regional) - 3} more regions)"
    
    text += " Critical for global brand consistency."
    
    return normalize_whitespace(text)

def generate_color_industry_text(color_data):
    """Generates concise industry suitability text."""
    mkt = color_data.get('marketing', {})
    suitability = mkt.get('industry_suitability', {})
    
    if not suitability: return "No industry-specific data."
    
    # Build concise industry notes
    notes = []
    for industry, note in list(suitability.items())[:3]:
        industry_name = industry.replace('_', ' ').title()
        notes.append(f"{industry_name}: {note}")
    
    return normalize_whitespace(" | ".join(notes))

def generate_color_summary_text(palette):
    """Generates concise palette synthesis."""
    if not palette: return "No palette detected."
    
    # Check for conflicts
    has_red = any(c['family'] == 'red' for c in palette)
    has_green = any(c['family'] == 'green' for c in palette)
    
    parts = []
    
    if has_red and has_green:
        parts.append("Red-green pairing detected—ensure sufficient separation for colorblind users.")
    
    # Check temperature
    warm_count = sum(1 for c in palette if "Warm" in c['scientific'].get('temperature', ''))
    cool_count = sum(1 for c in palette if "Cool" in c['scientific'].get('temperature', ''))
    
    if warm_count > cool_count:
        parts.append("Warm-dominant palette creates energy and approachability.")
    elif cool_count > warm_count:
        parts.append("Cool-dominant palette signals professionalism and calm.")
    else:
        parts.append("Balanced temperature palette offers versatile emotional range.")
    
    return normalize_whitespace(" ".join(parts)) if parts else "Palette analysis complete."
