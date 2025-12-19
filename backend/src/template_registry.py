import os
import json
import logging

logger = logging.getLogger(__name__)

class TemplateRegistry:
    def __init__(self):
        self._templates = {}
        # Load legacy/existing templates first
        self._load_legacy_registry()
        # Generate/Load dynamic theme templates
        self._generate_theme_templates()

    def _load_legacy_registry(self):
        # Assuming templates.json exists in ../templates/templates.json
        # Adjust path as necessary closer to app root or config
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            json_path = os.path.join(base_dir, 'templates', 'templates.json')
            
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    data = json.load(f)
                    for key, val in data.get('templates', {}).items():
                        # Standardize structure
                        self._templates[key] = {
                            "id": key,
                            "name": val.get('name', key.title()),
                            "category": "Classic", # Default category for legacy
                            "type": "reportlab", # Legacy render engine
                            "image": "/static/images/templates/resume-placeholder.png", # Placeholder
                            "css_path": val.get('css_path'),
                            "description": val.get('description', '')
                        }
        except Exception as e:
            logger.error(f"Failed to load legacy templates: {e}")

    def _generate_theme_templates(self):
        """
        Generates 50 CSS-based themes.
        Categories: Modern, Creative, Minimal, Professional, Academic
        """
        categories = ['Modern', 'Creative', 'Minimal', 'Professional', 'Academic']
        
        for i in range(1, 51):
            theme_id = f"theme-{i}"
            category = categories[i % 5]
            
            self._templates[theme_id] = {
                "id": theme_id,
                "name": f"{category} Style {i}",
                "category": category,
                "type": "html_css", # New render engine
                "image": f"https://placehold.co/300x400/e0e0e0/333333?text={category}+{i}",
                "css_path": f"/static/css/themes/theme-{i}.css",
                "description": f"A {category.lower()} design perfect for general use."
            }

    def get_all_templates(self):
        return list(self._templates.values())

    def get_template(self, template_id):
        return self._templates.get(template_id)

    def get_templates_by_category(self, category):
        return [t for t in self._templates.values() if t['category'].lower() == category.lower()]

# Singleton instance
registry = TemplateRegistry()
