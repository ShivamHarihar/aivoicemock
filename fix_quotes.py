with open(r'd:\AI Interview Folder\sampro-ai-interview\frontend\src\base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix escaped quotes
content = content.replace("\\'", "'")

with open(r'd:\AI Interview Folder\sampro-ai-interview\frontend\src\base.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed escaped quotes!")
