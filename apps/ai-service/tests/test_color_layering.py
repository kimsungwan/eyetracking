import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from color_psychology import analyze_color_psychology, recommend_cta_color

def test_color_layering():
    print("Testing Color Analysis Layering (Science vs Marketing)...\n")
    
    # Test 1: Analyze Red
    print("1. Analyzing Red (#FF0000)...")
    analysis = analyze_color_psychology("#FF0000")
    
    # Check Scientific Layer
    assert "scientific" in analysis, "Missing 'scientific' key"
    sci = analysis["scientific"]
    assert "luminance" in sci, "Missing 'luminance' in scientific"
    assert "hex" in sci, "Missing 'hex' in scientific"
    print(f"   [PASS] Scientific Data: {sci}")
    
    # Check Marketing Layer
    assert "marketing" in analysis, "Missing 'marketing' key"
    mkt = analysis["marketing"]
    assert "primary_emotion" in mkt, "Missing 'primary_emotion'"
    assert "cultural_variants" in mkt, "Missing 'cultural_variants'"
    assert "kr" in mkt["cultural_variants"], "Missing 'kr' cultural variant"
    print(f"   [PASS] Marketing Data: {mkt['primary_emotion']}, Cultural(KR): {mkt['cultural_variants']['kr']}")
    
    print("-" * 50)
    
    # Test 2: CTA Recommendation
    print("2. Testing CTA Recommendation...")
    rec = recommend_cta_color(industry="e-commerce", current_bg="#FFFFFF")
    
    # Check Structure
    assert "scientific" in rec, "Missing 'scientific' in CTA rec"
    assert "marketing" in rec, "Missing 'marketing' in CTA rec"
    
    # Check Logic
    assert rec["scientific"]["wcag_level"] in ["AA", "AAA"], "CTA recommendation failed WCAG check"
    assert len(rec["marketing"]["rationale"]) > 0, "Missing marketing rationale"
    
    print(f"   [PASS] Recommended: {rec['recommended_color']}")
    print(f"   [PASS] Science: {rec['scientific']['justification']}")
    print(f"   [PASS] Marketing: {rec['marketing']['rationale']}")
    
    print("\nAll tests passed!")

if __name__ == "__main__":
    test_color_layering()
