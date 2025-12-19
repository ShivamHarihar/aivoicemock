import os
import json

REPO_ROOT = os.getcwd()
SKIP_DIRS = {'.git', '.venv', 'node_modules', '__pycache__', '.vscode', '.gemini'}

def get_language(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext in ['.py']: return 'python'
    if ext in ['.js', '.jsx']: return 'javascript'
    if ext in ['.ts', '.tsx']: return 'typescript'
    if ext in ['.html', '.htm']: return 'html'
    if ext in ['.css', '.scss', '.sass']: return 'css'
    if ext in ['.json']: return 'json'
    if ext in ['.md']: return 'markdown'
    return 'unknown'

def get_label(path, filename, content):
    lower_path = path.lower()
    if 'template' in lower_path: return 'frontend-template'
    if 'css' in lower_path or 'style' in lower_path: return 'css'
    if 'js' in lower_path or 'script' in lower_path: return 'js'
    if 'backend' in lower_path and filename.endswith('.py'): return 'backend-python'
    if 'test' in lower_path: return 'tests'
    if 'static' in lower_path or 'assets' in lower_path: return 'static-asset'
    if 'pdf' in content.lower() or 'export' in content.lower(): return 'pdf-export'
    return 'unknown'

inventory = []

for root, dirs, files in os.walk(REPO_ROOT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for file in files:
        full_path = os.path.join(root, file)
        rel_path = os.path.relpath(full_path, REPO_ROOT)
        
        try:
            size = os.path.getsize(full_path)
            with open(full_path, 'r', errors='ignore') as f:
                content = f.read(200)
            
            lang = get_language(file)
            label = get_label(rel_path, file, content)
            
            inventory.append({
                'path': rel_path,
                'filesize': size,
                'language': lang,
                'first_200_chars': content,
                'label': label
            })
        except Exception as e:
            print(f"Error processing {rel_path}: {e}")

with open('analysis/project_inventory.json', 'w') as f:
    json.dump(inventory, f, indent=2)

print(f"Inventory generated with {len(inventory)} files.")
