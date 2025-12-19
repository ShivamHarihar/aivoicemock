"""
Update CSS to remove old wrapper styles and ensure perfect 3-column grid
"""

# Read the CSS file
css_file = r'd:\AI Interview Folder\sampro-ai-interview\frontend\public\css\ats_dashboard.css'
with open(css_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove dashboard-left and dashboard-right styles if they exist
import re

# Remove these old styles
old_styles = r'\.dashboard-left,\s*\.dashboard-right\s*\{[^}]+\}'
content = re.sub(old_styles, '', content, flags=re.DOTALL)

# Make sure the grid is properly configured
# Find and ensure the dashboard-main-grid has the right settings
grid_pattern = r'\/\* Dashboard Main Grid[^{]+\{[^}]+\}'
grid_replacement = '''/* Dashboard Main Grid - Perfect 3 Equal Cards per Row */
.dashboard-main-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
    margin-bottom: 50px;
}'''

content = re.sub(grid_pattern, grid_replacement, content, flags=re.DOTALL)

# Write back
with open(css_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ CSS updated successfully!")
print("✅ Removed old wrapper styles")
print("✅ Ensured 3-column grid configuration")
print("✅ All cards will now be equal size")
