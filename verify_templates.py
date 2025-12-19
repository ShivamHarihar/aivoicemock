import os
import sys
import logging

# Setup path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.src import pdf_generator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SAMPLE_MARKDOWN = """
# John Doe
**Software Engineer**

email@example.com | 123-456-7890 | New York, NY

## Summary
Experienced software engineer with a passion for building scalable applications.

## Experience
### Senior Developer
*Tech Corp*
*2020 - Present*
- Led a team of 5 developers.
- Improved performance by 50%.

## Skills
- Python, JavaScript, React, Flask
"""

def test_templates():
    templates = ['template-1', 'template-2', 'template-3', 'template-4', 'template-5']
    output_dir = 'verification_output'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for template_id in templates:
        logger.info(f"Testing template: {template_id}")
        try:
            pdf_bytes = pdf_generator.markdown_to_pdf(SAMPLE_MARKDOWN, template_id)
            
            output_path = os.path.join(output_dir, f"test_{template_id}.pdf")
            with open(output_path, 'wb') as f:
                f.write(pdf_bytes)
                
            size = os.path.getsize(output_path)
            logger.info(f"✅ Generated {output_path} ({size} bytes)")
            
            if size == 0:
                logger.error(f"❌ File is empty: {output_path}")
                
        except Exception as e:
            logger.error(f"❌ Failed to generate {template_id}: {e}")

if __name__ == "__main__":
    test_templates()
