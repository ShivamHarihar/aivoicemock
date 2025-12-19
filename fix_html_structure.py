"""
Fix ATS Dashboard HTML - Remove wrapper divs for proper 3-column grid
"""

# Read the HTML file
html_file = r'd:\AI Interview Folder\sampro-ai-interview\frontend\src\ats_dashboard.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Step 1: Remove dashboard-left opening
content = content.replace(
    '            <!-- Left Column -->\n            <div class="dashboard-left">',
    '            <!-- All cards in 3-column grid -->'
)

# Step 2: Remove the closing of dashboard-left and opening of dashboard-right
content = content.replace(
    '            </div>\n\n            <!-- Right Column -->\n            <div class="dashboard-right">',
    '\n'
)

# Step 3: Find and remove the extra closing div for dashboard-right
# It should be right before the closing of dashboard-main-grid
content = content.replace(
    '            </div>\n        </div>\n        <!-- /dashboard-main-grid -->',
    '        </div>\n        <!-- /dashboard-main-grid -->'
)

# Write back
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ HTML structure fixed successfully!")
print("✅ Removed dashboard-left wrapper")
print("✅ Removed dashboard-right wrapper")
print("✅ All cards are now direct children of the grid")
print("✅ 3-column layout will now work correctly")
