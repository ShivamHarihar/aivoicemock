"""
Quick test script to debug PDF generation
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

# Test markdown
test_markdown = """# John Doe
**Software Engineer** | john@example.com | (555) 123-4567

## Professional Summary
Experienced software engineer with 5+ years in web development.

## Skills
**Languages**: Python, JavaScript, Java
**Frameworks**: React, Flask, Django
**Tools**: Git, Docker, AWS

## Experience

### Senior Software Engineer
*Tech Corp | 2020 - Present*

- Led development of microservices architecture
- Improved system performance by 40%
- Mentored junior developers

### Software Engineer
*StartupCo | 2018 - 2020*

- Built RESTful APIs using Flask
- Implemented CI/CD pipelines
- Collaborated with cross-functional teams

## Education
**BS Computer Science** | University of Tech | 2018
"""

print("Testing PDF Generation...")
print("="*50)

# Test 1: Import check
print("\n[TEST 1] Checking imports...")
try:
    from backend.src import pdf_generator
    print("✅ pdf_generator imported")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Generate PDF
print("\n[TEST 2] Generating PDF...")
try:
    pdf_bytes = pdf_generator.markdown_to_pdf(test_markdown)
    print(f"✅ PDF generated: {len(pdf_bytes)} bytes")
    
    # Save to file for inspection
    output_path = "test_resume.pdf"
    with open(output_path, 'wb') as f:
        f.write(pdf_bytes)
    print(f"✅ PDF saved to: {output_path}")
    
except Exception as e:
    print(f"❌ PDF generation failed: {e}")
    import traceback
    traceback.print_exc()
    
    # Try fallback
    print("\n[TEST 3] Trying fallback simple PDF...")
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        import io
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, "Test PDF")
        c.save()
        
        pdf_bytes = buffer.getvalue()
        print(f"✅ Simple PDF generated: {len(pdf_bytes)} bytes")
        
        with open("test_simple.pdf", 'wb') as f:
            f.write(pdf_bytes)
        print("✅ Simple PDF saved to: test_simple.pdf")
        
    except Exception as e2:
        print(f"❌ Fallback also failed: {e2}")
        import traceback
        traceback.print_exc()

print("\n" + "="*50)
print("Test complete!")
