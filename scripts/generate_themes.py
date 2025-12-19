import os
import random

# Configuration
THEME_DIR = r"d:\newSamproProject\sampro-ai-interview\frontend\public\css\themes"

colors = [
    ("#2c3e50", "#e74c3c"), ("#333333", "#009688"), ("#1a237e", "#ffab00"), 
    ("#006064", "#00bcd4"), ("#263238", "#ff5722"), ("#3e2723", "#795548"),
    ("#000000", "#d50000"), ("#1b5e20", "#4caf50"), ("#311b92", "#673ab7"),
    ("#0d47a1", "#2196f3")
]
fonts = ["'Roboto', sans-serif", "'Open Sans', sans-serif", "'Lato', sans-serif", "'Merriweather', serif", "'Playfair Display', serif"]

def get_base_css(primary, secondary, font):
    return f"""
:root {{
    --primary-color: {primary};
    --secondary-color: {secondary};
    --text-main: #333333;
    --text-muted: #666666;
    --bg-body: #ffffff;
    --font-main: {font};
}}
body {{
    font-family: var(--font-main);
    color: var(--text-main);
    line-height: 1.6;
    margin: 0; 
    padding: 0;
    box-sizing: border-box;
}}
*, *::before, *::after {{ box-sizing: inherit; }}
h1, h2, h3, h4 {{ margin-top: 0; }}
a {{ text-decoration: none; color: inherit; }}
ul {{ padding-left: 1.2rem; margin: 0.5rem 0; }}
"""

def layout_classic(primary, secondary):
    return f"""
/* Layout: Classic (Centered Header, Linear) */
.resume-wrapper {{ padding: 2rem; max-width: 800px; margin: 0 auto; }}
.header {{ text-align: center; border-bottom: 2px solid var(--primary-color); padding-bottom: 1.5rem; margin-bottom: 2rem; }}
.header h1 {{ font-size: 2.5rem; color: var(--primary-color); margin-bottom: 0.5rem; text-transform: uppercase; }}
.header h3 {{ font-size: 1.2rem; font-weight: 400; color: var(--text-muted); }}
.contact-info {{ display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-top: 0.5rem; font-size: 0.9rem; }}

.section {{ margin-bottom: 2rem; }}
.section h2 {{ 
    color: var(--primary-color); 
    font-size: 1.5rem; 
    border-bottom: 1px solid #eee; 
    padding-bottom: 0.5rem; 
    margin-bottom: 1rem; 
}}

.experience-item, .education-item {{ margin-bottom: 1.5rem; }}
.item-header {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.3rem; }}
.item-title {{ font-weight: 700; font-size: 1.1rem; }}
.item-subtitle {{ color: var(--text-muted); font-style: italic; }}
.item-date {{ font-size: 0.9rem; color: var(--primary-color); font-weight: 500; }}

.skills-grid {{ display: flex; flex-wrap: wrap; gap: 0.5rem; }}
.skill-tag {{ background: #f5f5f5; padding: 0.3rem 0.8rem; border-radius: 4px; border: 1px solid #ddd; font-size: 0.9rem; }}
.skill-tag:hover {{ border-color: var(--primary-color); color: var(--primary-color); }}
"""

def layout_sidebar_left(primary, secondary):
    return f"""
/* Layout: Modern Sidebar Left */
body {{ background: #f0f0f0; }}
.resume-wrapper {{ 
    display: grid; 
    grid-template-columns: 280px 1fr; 
    min-height: 100vh; 
    background: white; 
    box-shadow: 0 0 20px rgba(0,0,0,0.05);
}}

.sidebar {{ 
    background: var(--primary-color); 
    color: white; 
    padding: 2rem; 
    text-align: left; 
}}
.sidebar .header h1 {{ color: white; font-size: 2rem; line-height: 1.2; margin-bottom: 0.5rem; }}
.sidebar .header h3 {{ color: rgba(255,255,255,0.8); font-size: 1.1rem; font-weight: 400; margin-bottom: 2rem; }}
.sidebar .contact-info {{ display: flex; flex-direction: column; gap: 0.8rem; font-size: 0.9rem; opacity: 0.9; margin-bottom: 3rem; }}
.sidebar .section h2 {{ color: white; border-bottom: 1px solid rgba(255,255,255,0.3); font-size: 1.2rem; margin-top: 2rem; }}

.main-content {{ padding: 3rem; }}
.main-content .section h2 {{ color: var(--primary-color); font-size: 1.8rem; text-transform: uppercase; letter-spacing: 2px; border-bottom: 2px solid var(--secondary-color); display: inline-block; padding-bottom: 5px; }}

.experience-item {{ margin-bottom: 2rem; position: relative; padding-left: 1.5rem; border-left: 2px solid #eee; }}
.experience-item::after {{ content: ''; position: absolute; left: -6px; top: 5px; width: 10px; height: 10px; background: var(--secondary-color); border-radius: 50%; }}
.item-header {{ margin-bottom: 0.5rem; }}
.item-title {{ font-weight: 700; font-size: 1.2rem; display: block; }}
.item-subtitle {{ color: #666; display: block; margin-bottom: 0.2rem; }}
.item-date {{ font-size: 0.85rem; color: #999; text-transform: uppercase; letter-spacing: 1px; }}

.skill-tag {{ display: block; margin-bottom: 0.5rem; }} /* In sidebar */
"""

def layout_minimal(primary, secondary):
    return f"""
/* Layout: Minimal Clean */
.resume-wrapper {{ padding: 3rem; max-width: 900px; margin: 0 auto; }}
.header {{ margin-bottom: 3rem; }}
.header h1 {{ font-weight: 300; font-size: 3.5rem; letter-spacing: -2px; margin-bottom: 0.5rem; }}
.header h3 {{ font-weight: 400; color: #666; letter-spacing: 2px; text-transform: uppercase; font-size: 1rem; }}
.contact-info {{ margin-top: 1.5rem; font-size: 0.9rem; color: #888; display: flex; gap: 2rem; }}

.section {{ margin-bottom: 2.5rem; display: grid; grid-template-columns: 200px 1fr; gap: 2rem; }}
.section h2 {{ 
    font-size: 1rem; 
    text-transform: uppercase; 
    letter-spacing: 2px; 
    color: #999; 
    font-weight: 600; 
    text-align: right; 
    margin: 0;
}}

.experience-item {{ margin-bottom: 1.5rem; }}
.item-title {{ font-weight: 700; font-size: 1.1rem; color: #000; }}
.item-subtitle {{ color: #444; }}
.item-date {{ font-size: 0.9rem; color: #999; }}

.skills-grid {{ display: flex; flex-wrap: wrap; gap: 1rem; }}
.skill-tag {{ border-bottom: 1px solid #ddd; padding-bottom: 2px; }}
"""

def layout_creative_header(primary, secondary):
    return f"""
/* Layout: Creative Header Block */
.header {{ 
    background: var(--primary-color); 
    color: white; 
    padding: 4rem 2rem; 
    text-align: center; 
    clip-path: polygon(0 0, 100% 0, 100% 85%, 50% 100%, 0 85%);
    margin-bottom: 3rem; 
}}
.resume-wrapper {{ max-width: 900px; margin: 0 auto; padding-bottom: 3rem; }}

.header h1 {{ font-size: 3rem; margin-bottom: 0.5rem; }}
.header h3 {{ opacity: 0.9; font-weight: 300; }}
.contact-info {{ justify-content: center; display: flex; gap: 1rem; margin-top: 1rem; opacity: 0.8; }}

.main-content {{ padding: 0 2rem; display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; }}
.section {{ break-inside: avoid; margin-bottom: 2rem; }}
.section.full-width {{ grid-column: 1 / -1; }} /* Summary */

.section h2 {{ 
    font-size: 1.8rem; 
    color: var(--primary-color); 
    font-weight: 900; 
    margin-bottom: 1.5rem; 
    position: relative; 
    display: inline-block;
}}
.section h2::before {{
    content: '';
    position: absolute;
    width: 100%;
    height: 10px;
    bottom: 5px;
    left: 0;
    background: var(--secondary-color);
    opacity: 0.3;
    z-index: -1;
}}

.experience-item {{ background: #f9f9f9; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid var(--primary-color); }}
.skill-tag {{ background: var(--primary-color); color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; display: inline-block; margin: 2px; }}
"""

def layout_professional_grid(primary, secondary):
    return f"""
/* Layout: Professional Grid */
.resume-wrapper {{ padding: 3rem; border-top: 10px solid var(--primary-color); max-width: 900px; margin: 0 auto; background: white; }}
.header {{ display: flex; justify-content: space-between; align-items: start; margin-bottom: 3rem; border-bottom: 1px solid #eee; padding-bottom: 2rem; }}
.header-text {{ flex: 1; }}
.header h1 {{ font-size: 2.5rem; color: #000; text-transform: uppercase; letter-spacing: -1px; }}
.header h3 {{ color: var(--primary-color); font-weight: 600; }}
.contact-info {{ text-align: right; display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.9rem; color: #555; }}

.main-grid {{ display: grid; grid-template-columns: 2fr 1fr; gap: 3rem; }}
.section h2 {{ 
    font-size: 1.1rem; 
    text-transform: uppercase; 
    letter-spacing: 1px; 
    color: var(--primary-color);
    border-left: 3px solid var(--secondary-color);
    padding-left: 1rem;
    margin-bottom: 1.5rem;
    background: #fcfcfc;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
}}

.experience-item {{ margin-bottom: 2rem; }}
.item-title {{ font-size: 1.2rem; font-weight: 700; }}
.item-date {{ float: right; color: #888; font-size: 0.9rem; }}

.skill-tag {{ display: block; margin-bottom: 0.5rem; font-weight: 600; color: #444; }}
"""

def generate_css(theme_id, layout_idx, primary, secondary, font):
    base = get_base_css(primary, secondary, font)
    
    layouts = [layout_classic, layout_sidebar_left, layout_minimal, layout_creative_header, layout_professional_grid]
    layout_func = layouts[layout_idx % len(layouts)]
    
    css = base + layout_func(primary, secondary)
    return css

def main():
    if not os.path.exists(THEME_DIR):
        os.makedirs(THEME_DIR)

    print("Generating 50 themes with 5 distinct layouts...")
    for i in range(1, 51):
        primary, secondary = colors[i % len(colors)]
        font = fonts[i % len(fonts)]
        layout_idx = (i - 1) % 5 # Rotate through layouts
        
        css_content = generate_css(f"theme-{i}", layout_idx, primary, secondary, font)
        
        filename = os.path.join(THEME_DIR, f"theme-{i}.css")
        with open(filename, "w") as f:
            f.write(css_content)
            
    print("Done! Themes generated.")

if __name__ == "__main__":
    main()
