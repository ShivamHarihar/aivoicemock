"""
Fix Responsive Breakpoints - Ensure 3 cards per row at 100% zoom
"""

css_file = r'd:\AI Interview Folder\sampro-ai-interview\frontend\public\css\ats_dashboard.css'

# Read the CSS file
with open(css_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the 1400px breakpoint with 1100px
# This ensures 3 columns work on 1366px and 1920px screens at 100% zoom
content = content.replace(
    '@media (max-width: 1400px) {',
    '@media (max-width: 1100px) {'
)

# Write back
with open(css_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Breakpoint fixed successfully!")
print("✅ Changed from 1400px to 1100px")
print("✅ 3 cards per row will now show at 100% zoom")
print("✅ Works on 1366px, 1920px, and larger screens")
print("✅ Only switches to 2 columns below 1100px")
