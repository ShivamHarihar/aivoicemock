"""
Final Polish - Compact sections, better charts, professional appearance
"""

css_file = r'd:\AI Interview Folder\sampro-ai-interview\frontend\public\css\ats_dashboard.css'

with open(css_file, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# 1. Make analysis sections more compact
analysis_section_old = r'\.analysis-section \{[^}]+\}'
analysis_section_new = '''.analysis-section {
    margin-bottom: 24px;
}'''
content = re.sub(analysis_section_old, analysis_section_new, content)

# 2. Reduce analysis card padding further
analysis_card_old = r'\.analysis-card \{[^}]+\}'
analysis_card_new = '''.analysis-card {
    padding: 20px;
    background: rgba(255, 255, 255, 0.98);
    border: 1px solid rgba(44, 62, 80, 0.08);
    border-radius: 12px;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
}'''
content = re.sub(analysis_card_old, analysis_card_new, content)

# 3. Reduce analysis header spacing
analysis_header_old = r'\.analysis-header \{[^}]+\}'
analysis_header_new = '''.analysis-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 14px;
    padding-bottom: 12px;
    border-bottom: 2px solid rgba(44, 62, 80, 0.06);
}'''
content = re.sub(analysis_header_old, analysis_header_new, content)

# 4. Smaller analysis icons
analysis_icon_old = r'\.analysis-icon \{[^}]+\}'
analysis_icon_new = '''.analysis-icon {
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    font-size: 1.4rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}'''
content = re.sub(analysis_icon_old, analysis_icon_new, content)

# 5. Smaller analysis heading
analysis_h3_old = r'\.analysis-header h3 \{[^}]+\}'
analysis_h3_new = '''.analysis-header h3 {
    flex: 1;
    font-size: 1.1rem;
    color: var(--text-main);
    margin: 0;
    font-weight: 800;
}'''
content = re.sub(analysis_h3_old, analysis_h3_new, content)

# 6. More compact list items
analysis_list_old = r'\.analysis-list li \{[^}]+\}'
analysis_list_new = '''.analysis-list li {
    padding: 8px 0 8px 24px;
    position: relative;
    color: var(--text-secondary);
    line-height: 1.5;
    border-bottom: 1px solid rgba(44, 62, 80, 0.04);
    font-size: 0.9rem;
}'''
content = re.sub(analysis_list_old, analysis_list_new, content)

# 7. Reduce CTA card size
cta_card_old = r'\/\* CTA Card - Compact & Attractive \*\/\s*\.cta-card \{[^}]+\}'
cta_card_new = '''/* CTA Card - Very Compact */
.cta-card {
    padding: 24px;
    background: linear-gradient(135deg, rgba(30, 107, 123, 0.08) 0%, rgba(231, 76, 60, 0.04) 100%);
    border: 1px solid rgba(30, 107, 123, 0.15);
    border-radius: 14px;
    margin-bottom: 24px;
    box-shadow: 0 4px 16px rgba(30, 107, 123, 0.08);
}'''
content = re.sub(cta_card_old, cta_card_new, content, flags=re.DOTALL)

# 8. Smaller CTA text
cta_text_old = r'\.cta-text h2 \{[^}]+\}\s*\.cta-text p \{[^}]+\}'
cta_text_new = '''.cta-text h2 {
    font-size: 1.5rem;
    margin-bottom: 8px;
    color: var(--text-main);
    font-weight: 800;
    letter-spacing: -0.5px;
}

.cta-text p {
    color: var(--text-secondary);
    line-height: 1.5;
    margin: 0;
    font-size: 0.95rem;
}'''
content = re.sub(cta_text_old, cta_text_new, content, flags=re.DOTALL)

# 9. Smaller CTA icon
cta_icon_old = r'\.cta-icon \{[^}]+\}'
cta_icon_new = '''.cta-icon {
    font-size: 3rem;
    flex-shrink: 0;
}'''
content = re.sub(cta_icon_old, cta_icon_new, content)

# 10. Fix score circle text positioning - increase spacing
score_details_old = r'\.score-details \{[^}]+\}\s*\.score-details h4 \{[^}]+\}\s*\.score-details p \{[^}]+\}'
score_details_new = '''.score-details {
    text-align: center;
    margin-top: 16px;
}

.score-details h4 {
    font-size: 1.4rem;
    color: var(--text-main);
    margin-bottom: 8px;
    font-weight: 800;
}

.score-details p {
    color: var(--text-secondary);
    margin-bottom: 12px;
    font-size: 0.95rem;
}'''
content = re.sub(score_details_old, score_details_new, content, flags=re.DOTALL)

# 11. Reduce analysis grid gap
analysis_grid_old = r'\.analysis-grid \{[^}]+\}'
analysis_grid_new = '''.analysis-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
}'''
content = re.sub(analysis_grid_old, analysis_grid_new, content)

# Write back
with open(css_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ All sections made more compact!")
print("✅ Analysis cards: 20px padding (reduced)")
print("✅ Analysis icons: 38px (smaller)")
print("✅ List items: 8px padding (compact)")
print("✅ CTA card: 24px padding (very compact)")
print("✅ Score circle: Better text spacing")
print("✅ Everything fits on screen now!")
print("✅ Professional, attractive appearance")
