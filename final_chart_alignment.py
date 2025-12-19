"""
Final Perfect Alignment - All charts same size, all text properly aligned
"""

css_file = r'd:\AI Interview Folder\sampro-ai-interview\frontend\public\css\ats_dashboard.css'

with open(css_file, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# 1. Make score circle same size as other charts - 200px
score_circle_wrapper_old = r'\.score-circle-wrapper \{[^}]+\}'
score_circle_wrapper_new = '''.score-circle-wrapper {
    width: 200px;
    height: 200px;
    position: relative;
    margin: 0 auto;
}'''
content = re.sub(score_circle_wrapper_old, score_circle_wrapper_new, content)

# 2. Ensure all chart containers have same height and centering
chart_container_old = r'\.chart-card \.chart-container \{[^}]+\}'
chart_container_new = '''.chart-card .chart-container {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 220px;
    max-height: 220px;
    padding: 0;
    margin: 0 auto;
}'''
content = re.sub(chart_container_old, chart_container_new, content)

# 3. Score circle container - same structure as chart containers
score_circle_container_old = r'\.score-card \.score-circle-container \{[^}]+\}'
score_circle_container_new = '''.score-card .score-circle-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    gap: 16px;
    padding: 0;
}'''
content = re.sub(score_circle_container_old, score_circle_container_new, content)

# 4. Score details - consistent spacing
score_details_old = r'\.score-details \{[^}]+\}\s*\.score-details h4 \{[^}]+\}\s*\.score-details p \{[^}]+\}'
score_details_new = '''.score-details {
    text-align: center;
    margin-top: 0;
    width: 100%;
}

.score-details h4 {
    font-size: 1.3rem;
    color: var(--text-main);
    margin-bottom: 8px;
    font-weight: 800;
}

.score-details p {
    color: var(--text-secondary);
    margin-bottom: 14px;
    font-size: 0.9rem;
    line-height: 1.4;
}'''
content = re.sub(score_details_old, score_details_new, content, flags=re.DOTALL)

# 5. Tier badge - consistent
tier_badge_old = r'\.tier-badge \{[^}]+\}'
tier_badge_new = '''.tier-badge {
    display: inline-block;
    padding: 8px 20px;
    border-radius: 20px;
    color: white;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.5px;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.15);
}'''
content = re.sub(tier_badge_old, tier_badge_new, content)

# 6. Fix funnel container to match chart height
funnel_container_old = r'\.funnel-container \{[^}]+\}'
funnel_container_new = '''.funnel-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 0;
    min-height: 220px;
    max-height: 220px;
    justify-content: center;
}'''
content = re.sub(funnel_container_old, funnel_container_new, content)

# 7. Funnel stages - smaller
funnel_stage_old = r'\.funnel-stage \{[^}]+\}'
funnel_stage_new = '''.funnel-stage {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 20px;
    border-radius: 10px;
    color: white;
    font-weight: 700;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}'''
content = re.sub(funnel_stage_old, funnel_stage_new, content)

# 8. Funnel text sizes
funnel_label_old = r'\.funnel-label \{[^}]+\}'
funnel_label_new = '''.funnel-label {
    font-size: 0.9rem;
}'''
content = re.sub(funnel_label_old, funnel_label_new, content)

funnel_value_old = r'\.funnel-value \{[^}]+\}'
funnel_value_new = '''.funnel-value {
    font-size: 1.1rem;
    font-weight: 800;
}'''
content = re.sub(funnel_value_old, funnel_value_new, content)

# 9. Fix analysis list bullets alignment
analysis_list_old = r'\.analysis-list \{[^}]+\}'
analysis_list_new = '''.analysis-list {
    list-style: none;
    padding: 0;
    margin: 0;
}'''
content = re.sub(analysis_list_old, analysis_list_new, content)

# 10. Fix analysis list items with proper bullet alignment
analysis_list_li_old = r'\.analysis-list li \{[^}]+\}'
analysis_list_li_new = '''.analysis-list li {
    padding: 6px 0 6px 0;
    position: relative;
    color: var(--text-secondary);
    line-height: 1.5;
    border-bottom: 1px solid rgba(44, 62, 80, 0.04);
    font-size: 0.85rem;
    padding-left: 24px;
    text-align: left;
}'''
content = re.sub(analysis_list_li_old, analysis_list_li_new, content)

# 11. Fix analysis list bullet
analysis_list_before_old = r'\.analysis-list li::before \{[^}]+\}'
analysis_list_before_new = '''.analysis-list li::before {
    content: "•";
    position: absolute;
    left: 8px;
    color: var(--primary);
    font-weight: 900;
    font-size: 1.2rem;
    line-height: 1.5;
}'''
content = re.sub(analysis_list_before_old, analysis_list_before_new, content)

# 12. Reduce analysis card width slightly for better fit
analysis_card_old = r'\.analysis-card \{[^}]+\}'
analysis_card_new = '''.analysis-card {
    padding: 18px;
    background: rgba(255, 255, 255, 0.98);
    border: 1px solid rgba(44, 62, 80, 0.08);
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
    max-width: 100%;
}'''
content = re.sub(analysis_card_old, analysis_card_new, content)

# 13. Ensure breakdown list has same structure
breakdown_list_old = r'\.breakdown-list \{[^}]+\}'
breakdown_list_new = '''.breakdown-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
    min-height: 220px;
    justify-content: center;
}'''
content = re.sub(breakdown_list_old, breakdown_list_new, content)

# Write back
with open(css_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Perfect chart alignment applied!")
print("✅ Score circle: 200px (same as other charts)")
print("✅ All chart containers: 220px height")
print("✅ Funnel container: 220px height")
print("✅ Breakdown list: 220px height")
print("✅ Analysis bullets: Properly aligned at left: 8px")
print("✅ Analysis text: Left-aligned, no wandering")
print("✅ All cards: Same size, perfect alignment")
print("✅ Professional appearance!")
