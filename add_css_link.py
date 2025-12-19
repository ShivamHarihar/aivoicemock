import re

# Read the base.html file
with open(r'd:\AI Interview Folder\sampro-ai-interview\frontend\src\base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the style.css link and add ats_dashboard.css after it
pattern = r'(<link rel="stylesheet" href="{{ url_for\(\'static\', filename=\'css/style\.css\'\) }}">\r?\n)'
replacement = r'\1    <link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/ats_dashboard.css\') }}">\n'

# Replace
new_content = re.sub(pattern, replacement, content)

# Write back
with open(r'd:\AI Interview Folder\sampro-ai-interview\frontend\src\base.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("CSS link added successfully!")
