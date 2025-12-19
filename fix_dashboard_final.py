import re

# Read the CSS file
css_file = r'd:\AI Interview Folder\sampro-ai-interview\frontend\public\css\ats_dashboard.css'
with open(css_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Remove the heading underline and simplify header
header_old = r'\/\* Page Header - Enhanced with Modern UI \*\/.*?line-height: 1\.6;\s*\}'
header_new = '''/* Page Header - Clean Modern UI */
.page-header {
    text-align: center;
    margin-bottom: 50px;
    padding: 0;
    background: transparent;
    border: none;
    box-shadow: none;
}

.page-header h1 {
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, #2C3E50 0%, #E74C3C 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 16px;
    letter-spacing: -1px;
    position: relative;
    display: inline-block;
}

/* Remove the underline */
.page-header h1::after {
    display: none;
}

.page-header .subtitle {
    font-size: 1.15rem;
    color: var(--text-secondary);
    font-weight: 400;
    margin-top: 0;
    line-height: 1.6;
}'''

content = re.sub(header_old, header_new, content, flags=re.DOTALL)

# Fix 2: Update dashboard grid for perfect 3-column layout
grid_old = r'\/\* Dashboard Main Grid.*?justify-content: center;\s*\}'
grid_new = '''/* Dashboard Main Grid - Perfect 3 Equal Cards per Row */
.dashboard-main-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
    margin-bottom: 50px;
    grid-auto-rows: 1fr;
}

/* Card Styles - All Equal Size */
.score-card,
.chart-card,
.breakdown-card {
    padding: 36px;
    background: rgba(255, 255, 255, 0.98);
    border: 1px solid rgba(44, 62, 80, 0.08);
    border-radius: 20px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    min-height: 480px;
    height: 100%;
}

/* Ensure chart containers fill available space */
.chart-card .chart-container {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 320px;
}

/* Score card specific */
.score-card .score-circle-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
}'''

content = re.sub(grid_old, grid_new, content, flags=re.DOTALL)

# Write back
with open(css_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ CSS fixed successfully!")
print("✅ Removed heading underline")
print("✅ Updated to perfect 3-column grid")
print("✅ All cards now equal size")
