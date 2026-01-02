import os
import re

# List of files to process
files = [
    "static/pricing-section_ko.html",
    "static/pricing-section_cn.html",
    "static/pricing-section_jp.html",
    "static/pricing-section.html",
    "static/science-section_ko.html",
    "static/science-section_cn.html",
    "static/science-section_jp.html",
    "static/science-section.html"
]

def fix_file(filepath):
    full_path = os.path.join(os.getcwd(), filepath)
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        return

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Row Fix
    # Add flexbox to row if not present
    if 'display: flex; align-items: stretch;' not in content:
        content = content.replace('<div class="row">', '<div class="row" style="display: flex; align-items: stretch;">')

    # 2. Col Fix
    # Add display: flex to columns (col-md-3 or col-md-4)
    # Look for style attribute containing margin-bottom: 30px;
    # Avoid adding if already present
    def add_flex_to_col(match):
        style_content = match.group(2)
        if 'display: flex' not in style_content:
            return f'{match.group(1)}"{style_content} display: flex;"'
        return match.group(0)

    content = re.sub(r'(class="col-md-[34]" style=)([^"]*)(")', add_flex_to_col, content)
    
    # 3. Card Div Fix
    # Add width: 100% to card divs (identified by border-radius: 16px)
    def add_width_to_card(match):
        style_content = match.group(1)
        if 'width: 100%' not in style_content:
            return f'style="{style_content} width: 100%;"'
        return match.group(0)
    
    content = re.sub(r'style="([^"]*border-radius: 16px;[^"]*)"', add_width_to_card, content)

    # 4. H3 Fix
    # Add min-height and centering to h3 titles
    # Pricing needs slightly more height (70px) than Science (60px)
    min_height = "70px" if "pricing" in filepath else "60px"
    
    def fix_h3(match):
        style_content = match.group(1)
        if 'min-height' not in style_content:
            return f'style="{style_content} min-height: {min_height}; display: flex; align-items: center; justify-content: center;"'
        return match.group(0)

    content = re.sub(r'<h3 style="([^"]*)"', fix_h3, content)

    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully fixed {filepath}")

if __name__ == "__main__":
    print("Starting layout fixes...")
    for f in files:
        try:
            fix_file(f)
        except Exception as e:
            print(f"Error fixing {f}: {e}")
    print("Completed layout fixes.")
