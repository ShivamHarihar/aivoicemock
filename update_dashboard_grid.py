import re

# Read the CSS file
with open(r'd:\AI Interview Folder\sampro-ai-interview\frontend\public\css\ats_dashboard.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the dashboard main grid section to ensure equal card heights
old_grid = r'\/\* Dashboard Main Grid - 3 Charts per Row \*\/\s*\.dashboard-main-grid \{\s*display: grid;\s*grid-template-columns: repeat\(3, 1fr\);\s*gap: 24px;\s*margin-bottom: 40px;\s*\}'

new_grid = '''/* Dashboard Main Grid - 3 Equal Cards per Row */
.dashboard-main-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 24px;
    margin-bottom: 40px;
    align-items: stretch;
}

/* Ensure all dashboard cards have equal height */
.dashboard-main-grid > .score-card,
.dashboard-main-grid > .chart-card,
.dashboard-main-grid > .breakdown-card {
    display: flex;
    flex-direction: column;
    height: 100%;
    min-height: 450px;
}'''

content = re.sub(old_grid, new_grid, content, flags=re.DOTALL)

# Also update the card styles to support flexbox
old_card_styles = r'\/\* Card Styles \*\/\s*\.score-card,\s*\.chart-card,\s*\.breakdown-card \{\s*padding: 32px;\s*background: rgba\(255, 255, 255, 0\.98\);\s*border: 1px solid rgba\(44, 62, 80, 0\.08\);\s*border-radius: 16px;\s*box-shadow: 0 4px 16px rgba\(0, 0, 0, 0\.04\);\s*transition: all 0\.3s ease;\s*\}'

new_card_styles = '''/* Card Styles - Equal Height */
.score-card,
.chart-card,
.breakdown-card {
    padding: 32px;
    background: rgba(255, 255, 255, 0.98);
    border: 1px solid rgba(44, 62, 80, 0.08);
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
}

/* Ensure chart containers fill available space */
.chart-card .chart-container {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
}'''

content = re.sub(old_card_styles, new_card_styles, content, flags=re.DOTALL)

# Write back
with open(r'd:\AI Interview Folder\sampro-ai-interview\frontend\public\css\ats_dashboard.css', 'w', encoding='utf-8') as f:
    f.write(content)

print("CSS updated successfully! All cards will now be equal size in rows of 3.")
