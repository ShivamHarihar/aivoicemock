"""
Perfect Alignment Fix - All cards, charts, and sections properly aligned
"""

css_file = r'd:\AI Interview Folder\sampro-ai-interview\frontend\public\css\ats_dashboard.css'

with open(css_file, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# 1. Fix card title spacing - consistent across all cards
card_title_old = r'\.card-title \{[^}]+\}'
card_title_new = '''.card-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--text-main);
    margin-bottom: 20px;
    letter-spacing: -0.5px;
    min-height: 30px;
}'''
content = re.sub(card_title_old, card_title_new, content)

# 2. Fix card header spacing - consistent
card_header_old = r'\.card-header \{[^}]+\}'
card_header_new = '''.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    min-height: 30px;
}'''
content = re.sub(card_header_old, card_header_new, content)

# 3. Ensure all cards have consistent internal structure
score_card_old = r'\.score-card,\s*\.chart-card,\s*\.breakdown-card\s*\{[^}]+\}'
score_card_new = '''.score-card,
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
content = re.sub(score_card_old, score_card_new, content, flags=re.DOTALL)

# 4. Fix chart container to be consistent
chart_container_old = r'\.chart-card \.chart-container \{[^}]+\}'
chart_container_new = '''.chart-card .chart-container {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 240px;
    max-height: 240px;
    padding: 10px 0;
}'''
content = re.sub(chart_container_old, chart_container_new, content)

# 5. Fix score circle container alignment
score_circle_container_old = r'\.score-card \.score-circle-container \{[^}]+\}'
score_circle_container_new = '''.score-card .score-circle-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 10px 0;
}'''
content = re.sub(score_circle_container_old, score_circle_container_new, content)

# 6. Reduce analysis section even more
analysis_section_old = r'\.analysis-section \{[^}]+\}'
analysis_section_new = '''.analysis-section {
    margin-bottom: 20px;
}'''
content = re.sub(analysis_section_old, analysis_section_new, content)

# 7. Make analysis cards even more compact
analysis_card_old = r'\.analysis-card \{[^}]+\}'
analysis_card_new = '''.analysis-card {
    padding: 16px;
    background: rgba(255, 255, 255, 0.98);
    border: 1px solid rgba(44, 62, 80, 0.08);
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
}'''
content = re.sub(analysis_card_old, analysis_card_new, content)

# 8. Smaller analysis header
analysis_header_old = r'\.analysis-header \{[^}]+\}'
analysis_header_new = '''.analysis-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 2px solid rgba(44, 62, 80, 0.06);
}'''
content = re.sub(analysis_header_old, analysis_header_new, content)

# 9. Even smaller analysis icons
analysis_icon_old = r'\.analysis-icon \{[^}]+\}'
analysis_icon_new = '''.analysis-icon {
    width: 34px;
    height: 34px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    font-size: 1.2rem;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    flex-shrink: 0;
}'''
content = re.sub(analysis_icon_old, analysis_icon_new, content)

# 10. Smaller analysis heading
analysis_h3_old = r'\.analysis-header h3 \{[^}]+\}'
analysis_h3_new = '''.analysis-header h3 {
    flex: 1;
    font-size: 1rem;
    color: var(--text-main);
    margin: 0;
    font-weight: 800;
}'''
content = re.sub(analysis_h3_old, analysis_h3_new, content)

# 11. Smaller analysis count badge
analysis_count_old = r'\.analysis-count \{[^}]+\}'
analysis_count_new = '''.analysis-count {
    background: var(--primary);
    color: white;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 800;
    flex-shrink: 0;
}'''
content = re.sub(analysis_count_old, analysis_count_new, content)

# 12. Very compact list items
analysis_list_old = r'\.analysis-list li \{[^}]+\}'
analysis_list_new = '''.analysis-list li {
    padding: 6px 0 6px 20px;
    position: relative;
    color: var(--text-secondary);
    line-height: 1.4;
    border-bottom: 1px solid rgba(44, 62, 80, 0.04);
    font-size: 0.85rem;
}'''
content = re.sub(analysis_list_old, analysis_list_new, content)

# 13. Reduce analysis grid gap
analysis_grid_old = r'\.analysis-grid \{[^}]+\}'
analysis_grid_new = '''.analysis-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
}'''
content = re.sub(analysis_grid_old, analysis_grid_new, content)

# 14. Make CTA card very compact
cta_card_old = r'\/\* CTA Card - Very Compact \*\/\s*\.cta-card \{[^}]+\}'
cta_card_new = '''/* CTA Card - Ultra Compact */
.cta-card {
    padding: 20px;
    background: linear-gradient(135deg, rgba(30, 107, 123, 0.08) 0%, rgba(231, 76, 60, 0.04) 100%);
    border: 1px solid rgba(30, 107, 123, 0.15);
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0 3px 12px rgba(30, 107, 123, 0.08);
}'''
content = re.sub(cta_card_old, cta_card_new, content, flags=re.DOTALL)

# 15. Smaller CTA content
cta_content_old = r'\.cta-content \{[^}]+\}'
cta_content_new = '''.cta-content {
    display: flex;
    align-items: center;
    gap: 16px;
}'''
content = re.sub(cta_content_old, cta_content_new, content)

# 16. Smaller CTA icon
cta_icon_old = r'\.cta-icon \{[^}]+\}'
cta_icon_new = '''.cta-icon {
    font-size: 2.5rem;
    flex-shrink: 0;
}'''
content = re.sub(cta_icon_old, cta_icon_new, content)

# 17. Smaller CTA text
cta_text_old = r'\.cta-text h2 \{[^}]+\}\s*\.cta-text p \{[^}]+\}'
cta_text_new = '''.cta-text h2 {
    font-size: 1.3rem;
    margin-bottom: 6px;
    color: var(--text-main);
    font-weight: 800;
    letter-spacing: -0.5px;
}

.cta-text p {
    color: var(--text-secondary);
    line-height: 1.4;
    margin: 0;
    font-size: 0.9rem;
}'''
content = re.sub(cta_text_old, cta_text_new, content, flags=re.DOTALL)

# 18. Smaller CTA button
cta_button_old = r'\.cta-button \{[^}]+\}'
cta_button_new = '''.cta-button {
    padding: 10px 20px;
    background: var(--primary);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 0.9rem;
    white-space: nowrap;
}'''
content = re.sub(cta_button_old, cta_button_new, content)

# Write back
with open(css_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Perfect alignment applied!")
print("✅ All card titles: 30px min-height")
print("✅ All chart containers: 240px height")
print("✅ Analysis cards: 16px padding (ultra compact)")
print("✅ Analysis icons: 34px (very small)")
print("✅ Analysis text: 0.85rem (compact)")
print("✅ CTA card: 20px padding (ultra compact)")
print("✅ CTA icon: 2.5rem (smaller)")
print("✅ Everything perfectly aligned!")
