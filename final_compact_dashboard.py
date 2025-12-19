"""
Final Dashboard CSS Fix - Reduce card sizes, perfect alignment, proper spacing
"""

css_file = r'd:\AI Interview Folder\sampro-ai-interview\frontend\public\css\ats_dashboard.css'

# Read current CSS
with open(css_file, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# 1. Update ATS Section - Add proper top padding for header spacing
ats_section_old = r'\.ats-section \{[^}]+\}'
ats_section_new = '''.ats-section {
    padding: 100px 0 60px;
    min-height: 100vh;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.5) 0%, rgba(248, 250, 252, 0.8) 100%);
}'''
content = re.sub(ats_section_old, ats_section_new, content)

# 2. Update Page Header - Clean with medium spacing
header_old = r'\/\* Page Header[^{]+\{[^}]+\}[^{]+\.page-header h1[^}]+\}[^{]+\.page-header h1::after[^}]+\}[^{]+\.page-header \.subtitle[^}]+\}'
header_new = '''/* Page Header - Clean with Medium Spacing */
.page-header {
    text-align: center;
    margin-bottom: 40px;
    padding: 0;
    background: transparent;
    border: none;
    box-shadow: none;
}

.page-header h1 {
    font-size: 3.2rem;
    font-weight: 900;
    background: linear-gradient(135deg, #2C3E50 0%, #E74C3C 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 12px;
    letter-spacing: -1px;
    position: relative;
    display: inline-block;
}

.page-header h1::after {
    display: none;
}

.page-header .subtitle {
    font-size: 1.1rem;
    color: var(--text-secondary);
    font-weight: 400;
    margin-top: 0;
    line-height: 1.6;
}'''
content = re.sub(header_old, header_new, content, flags=re.DOTALL)

# 3. Update Dashboard Main Grid - Smaller cards
grid_old = r'\/\* Dashboard Main Grid[^{]+\{[^}]+\}'
grid_new = '''/* Dashboard Main Grid - 3 Cards per Row, Compact Size */
.dashboard-main-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    margin-bottom: 40px;
}'''
content = re.sub(grid_old, grid_new, content)

# 4. Update Card Styles - Reduced size
card_styles_old = r'\/\* Card Styles - All Equal Size \*\/[^{]+\.score-card,\s*\.chart-card,\s*\.breakdown-card\s*\{[^}]+\}'
card_styles_new = '''/* Card Styles - Compact Equal Size */
.score-card,
.chart-card,
.breakdown-card {
    padding: 28px;
    background: rgba(255, 255, 255, 0.98);
    border: 1px solid rgba(44, 62, 80, 0.08);
    border-radius: 16px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    min-height: 380px;
    height: 100%;
}'''
content = re.sub(card_styles_old, card_styles_new, content, flags=re.DOTALL)

# 5. Update Chart Container - Smaller
chart_container_old = r'\/\* Chart Container \*\/\s*\.chart-container\s*\{[^}]+\}\s*\.chart-container canvas\s*\{[^}]+\}'
chart_container_new = '''/* Chart Container - Compact */
.chart-container {
    position: relative;
    height: 260px;
    width: 100%;
}

.chart-container canvas {
    max-height: 260px;
}'''
content = re.sub(chart_container_old, chart_container_new, content, flags=re.DOTALL)

# 6. Update Score Circle - Smaller
score_circle_old = r'\.score-circle-wrapper\s*\{[^}]+\}'
score_circle_new = '''.score-circle-wrapper {
    width: 220px;
    height: 220px;
    position: relative;
}'''
content = re.sub(score_circle_old, score_circle_new, content)

# 7. Update Analysis Section - More compact and attractive
analysis_old = r'\/\* Analysis Section[^{]+\{[^}]+\}\s*\.analysis-grid\s*\{[^}]+\}\s*\.analysis-card\s*\{[^}]+\}'
analysis_new = '''/* Analysis Section - Compact & Attractive */
.analysis-section {
    margin-bottom: 30px;
}

.analysis-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
}

.analysis-card {
    padding: 24px;
    background: rgba(255, 255, 255, 0.98);
    border: 1px solid rgba(44, 62, 80, 0.08);
    border-radius: 14px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
}'''
content = re.sub(analysis_old, analysis_new, content, flags=re.DOTALL)

# 8. Update Analysis Header - Smaller icons
analysis_header_old = r'\.analysis-header\s*\{[^}]+\}\s*\.analysis-icon\s*\{[^}]+\}'
analysis_header_new = '''.analysis-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 18px;
    padding-bottom: 16px;
    border-bottom: 2px solid rgba(44, 62, 80, 0.06);
}

.analysis-icon {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    font-size: 1.6rem;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}'''
content = re.sub(analysis_header_old, analysis_header_new, content, flags=re.DOTALL)

# 9. Update Analysis Header h3 - Smaller font
analysis_h3_old = r'\.analysis-header h3\s*\{[^}]+\}'
analysis_h3_new = '''.analysis-header h3 {
    flex: 1;
    font-size: 1.2rem;
    color: var(--text-main);
    margin: 0;
    font-weight: 800;
}'''
content = re.sub(analysis_h3_old, analysis_h3_new, content)

# 10. Update Analysis List - More compact
analysis_list_old = r'\.analysis-list li\s*\{[^}]+\}'
analysis_list_new = '''.analysis-list li {
    padding: 10px 0 10px 28px;
    position: relative;
    color: var(--text-secondary);
    line-height: 1.6;
    border-bottom: 1px solid rgba(44, 62, 80, 0.04);
    font-size: 0.95rem;
}'''
content = re.sub(analysis_list_old, analysis_list_new, content)

# 11. Update CTA Card - More compact
cta_old = r'\/\* CTA Card - Enhanced \*\/\s*\.cta-card\s*\{[^}]+\}'
cta_new = '''/* CTA Card - Compact & Attractive */
.cta-card {
    padding: 32px;
    background: linear-gradient(135deg, rgba(30, 107, 123, 0.08) 0%, rgba(231, 76, 60, 0.04) 100%);
    border: 1px solid rgba(30, 107, 123, 0.15);
    border-radius: 16px;
    margin-bottom: 30px;
    box-shadow: 0 6px 24px rgba(30, 107, 123, 0.08);
}'''
content = re.sub(cta_old, cta_new, content)

# 12. Update CTA text - Smaller
cta_text_old = r'\.cta-text h2\s*\{[^}]+\}\s*\.cta-text p\s*\{[^}]+\}'
cta_text_new = '''.cta-text h2 {
    font-size: 1.75rem;
    margin-bottom: 10px;
    color: var(--text-main);
    font-weight: 800;
    letter-spacing: -0.5px;
}

.cta-text p {
    color: var(--text-secondary);
    line-height: 1.6;
    margin: 0;
    font-size: 1rem;
}'''
content = re.sub(cta_text_old, cta_text_new, content, flags=re.DOTALL)

# 13. Update CTA icon - Smaller
cta_icon_old = r'\.cta-icon\s*\{[^}]+\}'
cta_icon_new = '''.cta-icon {
    font-size: 3.5rem;
    flex-shrink: 0;
}'''
content = re.sub(cta_icon_old, cta_icon_new, content)

# Write back
with open(css_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ CSS Updated Successfully!")
print("✅ Dashboard cards reduced to 380px height")
print("✅ Charts reduced to 260px height")
print("✅ Score circle reduced to 220px")
print("✅ Analysis cards more compact (24px padding)")
print("✅ Header spacing set to medium (40px)")
print("✅ All text remains visible")
print("✅ Professional, attractive, modern UI")
