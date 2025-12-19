"""
Test Script for Multiple Resume Templates Feature
Tests all 5 templates with sample resume content
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

# Sample resume markdown
test_markdown = """# Sarah Johnson
**Senior Software Engineer** | sarah.johnson@email.com | (555) 123-4567 | linkedin.com/in/sarahjohnson

## Professional Summary
Results-driven Senior Software Engineer with 8+ years of experience in full-stack development, cloud architecture, and team leadership. Proven track record of delivering scalable solutions and mentoring junior developers.

## Technical Skills
**Languages**: Python, JavaScript, TypeScript, Java, Go
**Frameworks**: React, Node.js, Django, Flask, Spring Boot
**Cloud & DevOps**: AWS (EC2, S3, Lambda), Docker, Kubernetes, CI/CD
**Databases**: PostgreSQL, MongoDB, Redis
**Tools**: Git, JIRA, Jenkins, Terraform

## Professional Experience

### Senior Software Engineer
*TechCorp Inc. | San Francisco, CA | 2020 - Present*

- Led development of microservices architecture serving 2M+ daily active users
- Reduced system latency by 45% through optimization and caching strategies
- Mentored team of 5 junior engineers, improving code quality by 60%
- Implemented CI/CD pipeline reducing deployment time from 4 hours to 15 minutes
- Architected real-time analytics dashboard using React and WebSockets
- Collaborated with product team to define technical requirements for new features

### Software Engineer
*StartupXYZ | San Francisco, CA | 2018 - 2020*

- Built RESTful APIs handling 100K+ requests per day
- Developed responsive web applications using React and TypeScript
- Integrated third-party payment systems (Stripe, PayPal)
- Implemented automated testing achieving 85% code coverage
- Participated in agile sprints and daily stand-ups

### Junior Developer
*Digital Solutions Co. | Remote | 2016 - 2018*

- Developed and maintained client websites using HTML, CSS, JavaScript
- Created database schemas and queries for e-commerce platforms
- Fixed bugs and improved existing codebases
- Provided technical support to clients

## Education
**Bachelor of Science in Computer Science**
University of California, Berkeley | 2012 - 2016
GPA: 3.8/4.0

## Certifications
- AWS Certified Solutions Architect - Associate
- Google Cloud Professional Developer

## Projects
**Open Source Contributor**
- Active contributor to popular Python libraries with 500+ GitHub stars
- Maintained documentation and resolved community issues
"""

def test_template(template_id, template_name):
    """Test a specific template"""
    print(f"\n{'='*60}")
    print(f"Testing {template_name} Template (ID: {template_id})")
    print(f"{'='*60}")
    
    try:
        from backend.src import pdf_generator
        
        print(f"✅ Generating PDF with '{template_id}' template...")
        pdf_bytes = pdf_generator.markdown_to_pdf(test_markdown, template_id=template_id)
        
        print(f"✅ PDF generated: {len(pdf_bytes)} bytes")
        
        # Save to file
        output_file = f"test_resume_{template_id}.pdf"
        with open(output_file, 'wb') as f:
            f.write(pdf_bytes)
        
        print(f"✅ PDF saved to: {output_file}")
        print(f"✅ {template_name} template: PASSED")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing {template_name} template: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all template tests"""
    print("\n" + "="*60)
    print("MULTIPLE RESUME TEMPLATES - TEST SUITE")
    print("="*60)
    
    templates = [
        ('template-1', 'Template 1'),
        ('template-2', 'Template 2'),
        ('template-3', 'Template 3'),
        ('template-4', 'Template 4'),
        ('template-5', 'Template 5')
    ]
    
    results = {}
    
    for template_id, template_name in templates:
        success = test_template(template_id, template_name)
        results[template_id] = success
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for template_id, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{template_id.ljust(15)}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All templates working correctly!")
    else:
        print(f"\n⚠️ {total - passed} template(s) failed")
        sys.exit(1)

if __name__ == '__main__':
    main()
