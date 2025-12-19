import pytest
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.src.pdf_generator import markdown_to_pdf
from backend.src.docx_generator import markdown_to_docx

SAMPLE_MARKDOWN = """
# John Doe
**Software Engineer**

## Experience
- Built amazing things
- Fixed critical bugs

## Skills
- Python, JavaScript, Docker
"""

def test_pdf_generation_fallback():
    """Test that PDF generation returns bytes even if WeasyPrint is missing (fallback)"""
    pdf_bytes = markdown_to_pdf(SAMPLE_MARKDOWN, template_id='modern')
    assert pdf_bytes is not None
    assert len(pdf_bytes) > 0
    assert pdf_bytes.startswith(b'%PDF')

def test_docx_generation():
    """Test that DOCX generation returns bytes"""
    docx_bytes = markdown_to_docx(SAMPLE_MARKDOWN, template_id='modern')
    assert docx_bytes is not None
    assert len(docx_bytes) > 0
    # Check for DOCX magic number/zip header
    assert docx_bytes.startswith(b'PK')

if __name__ == "__main__":
    # Manual run if pytest not installed
    try:
        test_pdf_generation_fallback()
        print("PDF Test Passed")
        test_docx_generation()
        print("DOCX Test Passed")
    except Exception as e:
        print(f"Test Failed: {e}")
