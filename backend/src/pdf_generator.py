import os
import re
import logging
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, 
    Table, TableStyle, ListFlowable, ListItem
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import FrameBreak

# Configure logger
logger = logging.getLogger(__name__)

class ResumeParser:
    def __init__(self, markdown_text):
        self.markdown = markdown_text
        self.sections = {}
        self.parse()

    def parse(self):
        lines = self.markdown.split('\n')
        current_section = None
        content_lines = []
        
        def save_section():
            if current_section and content_lines:
                self.sections[current_section] = '\n'.join(content_lines).strip()

        # Extract name (first line with #)
        name_match = re.search(r'^#\s+(.+)', self.markdown, re.MULTILINE)
        self.sections['name'] = name_match.group(1).strip() if name_match else 'Your Name'

        # Extract title (first bold text **)
        title_match = re.search(r'\*\*(.+?)\*\*', self.markdown)
        self.sections['title'] = title_match.group(1).strip() if title_match else ''

        # Extract contact info
        self.sections['contact'] = self.extract_contact()

        for line in lines:
            line = line.strip()
            if line.startswith('## '):
                save_section()
                raw_name = line[3:].strip().lower()
                current_section = re.sub(r'\s+', '_', raw_name)
                content_lines = []
            elif current_section:
                content_lines.append(line)
        
        save_section()

    def extract_contact(self):
        contact = {}
        email_match = re.search(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', self.markdown)
        if email_match: contact['email'] = email_match.group(1)
            
        phone_match = re.search(r'(\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9})', self.markdown)
        if phone_match: contact['phone'] = phone_match.group(1)
            
        linkedin_match = re.search(r'(linkedin\.com\/in\/[^\s)]+)', self.markdown)
        if linkedin_match: contact['linkedin'] = linkedin_match.group(1)
            
        location_match = re.search(r'([A-Z][a-z]+,\s*[A-Z]{2}|[A-Z][a-z]+,\s*[A-Z][a-z]+)', self.markdown)
        if location_match: contact['location'] = location_match.group(1)
            
        return contact

    def get_section(self, keys):
        """Get section content with flexible matching"""
        if isinstance(keys, str): keys = [keys]
        
        # Try exact match first
        for key in keys:
            if key in self.sections:
                return self.sections[key]
        
        # Try lowercase match
        for key in keys:
            key_lower = key.lower().replace(' ', '_')
            if key_lower in self.sections:
                return self.sections[key_lower]
        
        # Try partial match (contains)
        for key in keys:
            key_lower = key.lower()
            for section_name in self.sections.keys():
                if key_lower in section_name or section_name in key_lower:
                    return self.sections[section_name]
        
        # Try common variations
        variation_map = {
            'experience': ['professional_experience', 'work_experience', 'employment', 'work_history'],
            'skills': ['technical_skills', 'core_competencies', 'key_skills', 'expertise'],
            'education': ['academic_background', 'qualifications', 'academic_qualifications'],
            'projects': ['key_projects', 'notable_projects', 'project_experience'],
            'summary': ['professional_summary', 'profile', 'about', 'professional_profile'],
            'certifications': ['certificates', 'professional_certifications']
        }
        
        for key in keys:
            key_lower = key.lower().replace(' ', '_')
            if key_lower in variation_map:
                for variation in variation_map[key_lower]:
                    if variation in self.sections:
                        return self.sections[variation]
        
        return ""

class PDFGenerator:
    def __init__(self, markdown_text, template_id='modern'):
        self.parser = ResumeParser(markdown_text)
        self.template_id = template_id
        self.styles = getSampleStyleSheet()
        self.setup_styles()

    def setup_styles(self):
        """Define custom styles based on template"""
        # Base colors
        self.colors = {
            'primary': colors.black,
            'secondary': colors.grey,
            'accent': colors.lightgrey,
            'text': colors.black,
            'bg_sidebar': colors.white
        }

        # Template Specific Colors
        if self.template_id in ['template-1', 'template-8', 'template-9']: # Dark Sidebar
            self.colors['bg_sidebar'] = colors.HexColor('#1f2a33')
            self.colors['text_sidebar'] = colors.white
            self.colors['primary'] = colors.HexColor('#1f2a33')
            self.colors['header_text'] = colors.white
            
        elif self.template_id == 'template-2': # Split Column
            self.colors['primary'] = colors.black
            self.colors['header_bg'] = colors.black
            self.colors['header_text'] = colors.white
            
        elif self.template_id in ['template-3', 'template-6', 'template-7', 'template-10', 'template-13', 'template-14']: # Single / Simple
            self.colors['primary'] = colors.HexColor('#333333')
            
        elif self.template_id == 'template-4': # Teal
            self.colors['bg_sidebar'] = colors.HexColor('#004d40')
            self.colors['text_sidebar'] = colors.HexColor('#e0f2f1')
            self.colors['primary'] = colors.HexColor('#004d40')
            self.colors['accent'] = colors.HexColor('#80cbc4')
            self.colors['header_text'] = colors.white
            
        elif self.template_id in ['template-5', 'template-15']: # Blue Header
            self.colors['header_bg'] = colors.HexColor('#0b4ea2') if self.template_id == 'template-5' else colors.HexColor('#2c3e50')
            self.colors['header_text'] = colors.white
            self.colors['primary'] = self.colors['header_bg']
            self.colors['bg_sidebar'] = colors.HexColor('#f8f9fa')
            
        elif self.template_id in ['template-11', 'template-12']: # Mint Sidebar
            self.colors['bg_sidebar'] = colors.HexColor('#E6EDE9')
            self.colors['text_sidebar'] = colors.black
            self.colors['primary'] = colors.HexColor('#6B8E23') if self.template_id == 'template-11' else colors.black
            self.colors['header_text'] = colors.black

        # Create Custom Paragraph Styles
        self.styles.add(ParagraphStyle(
            name='NameTitle', 
            fontName='Helvetica-Bold', 
            fontSize=24, 
            leading=28,
            textColor=self.colors.get('header_text', self.colors['primary'])
        ))
        
        self.styles.add(ParagraphStyle(
            name='RoleTitle',
            fontName='Helvetica',
            fontSize=14,
            leading=18,
            textColor=self.colors.get('header_text', self.colors['secondary'])
        ))

        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            fontName='Helvetica-Bold',
            fontSize=16,
            leading=20,
            spaceBefore=12,
            spaceAfter=6,
            textColor=self.colors['primary'],
            textTransform='uppercase'
        ))

        self.styles.add(ParagraphStyle(
            name='SidebarHeader',
            parent=self.styles['SectionHeader'],
            fontSize=14,
            textColor=self.colors.get('text_sidebar', self.colors['primary'])
        ))

        self.styles.add(ParagraphStyle(
            name='SidebarText',
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=self.colors.get('text_sidebar', colors.black)
        ))

        self.styles.add(ParagraphStyle(
            name='MainText',
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.black
        ))
        
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=14,
            spaceBefore=8,
            textColor=colors.black
        ))

    def md_to_flowables(self, text, style_name='MainText'):
        """Convert markdown text to ReportLab flowables"""
        if not text: return []
        
        flowables = []
        style = self.styles[style_name]
        
        for line in text.split('\n'):
            line = line.strip()
            if not line: continue
            
            if line.startswith('### '):
                flowables.append(Paragraph(line[4:], self.styles['JobTitle']))
            elif line.startswith('- ') or line.startswith('* '):
                # Handle bullets
                bullet_text = line[2:]
                # Bold processing within text
                bullet_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', bullet_text)
                
                flowables.append(Paragraph(f"• {bullet_text}", style))
            else:
                text_content = line
                text_content = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text_content)
                flowables.append(Paragraph(text_content, style))
        
        return flowables

    def draw_background(self, canvas, doc):
        """Draw background colors for sidebars/headers"""
        canvas.saveState()
        
        if self.template_id in ['template-1', 'template-8', 'template-9']:
            # Dark Left Sidebar
            canvas.setFillColor(self.colors['bg_sidebar'])
            canvas.rect(0, 0, 70*mm, 297*mm, fill=1, stroke=0)
            
        elif self.template_id == 'template-2':
            # Header Band
            canvas.setFillColor(self.colors['header_bg'])
            canvas.rect(0, 250*mm, 210*mm, 47*mm, fill=1, stroke=0)
            # Right Sidebar (lighter grey)
            canvas.setFillColor(colors.HexColor('#fafafa'))
            canvas.rect(130*mm, 0, 80*mm, 250*mm, fill=1, stroke=0)
            
        elif self.template_id == 'template-4':
            # Teal Left Sidebar
            canvas.setFillColor(self.colors['bg_sidebar'])
            canvas.rect(0, 0, 70*mm, 297*mm, fill=1, stroke=0)
            
        elif self.template_id in ['template-5', 'template-15']:
            # Blue Header Band
            canvas.setFillColor(self.colors['header_bg'])
            canvas.rect(0, 260*mm, 210*mm, 37*mm, fill=1, stroke=0)
            # Right Sidebar Box
            canvas.setFillColor(self.colors['bg_sidebar'])
            # Draw a rect for the sidebar area, but with margins
            canvas.rect(140*mm, 20*mm, 60*mm, 230*mm, fill=1, stroke=0)

        elif self.template_id in ['template-11', 'template-12']:
            # Mint Left Sidebar
            canvas.setFillColor(self.colors['bg_sidebar'])
            canvas.rect(0, 0, 70*mm, 297*mm, fill=1, stroke=0)
            
        canvas.restoreState()

    def generate(self):
        buffer = io.BytesIO()
        doc = BaseDocTemplate(buffer, pagesize=A4, rightMargin=0, leftMargin=0, topMargin=0, bottomMargin=0)
        
        from reportlab.platypus import NextPageTemplate

        # --- Frames & Templates Definition ---
        
        # 1. Sidebar Left (Templates 1 & 4)
        frames_sidebar_left = [
            Frame(0, 0, 70*mm, 297*mm, leftPadding=10*mm, rightPadding=5*mm, topPadding=10*mm, bottomPadding=10*mm, id='sidebar'),
            Frame(70*mm, 0, 140*mm, 297*mm, leftPadding=10*mm, rightPadding=10*mm, topPadding=10*mm, bottomPadding=10*mm, id='main')
        ]
        
        # 2. Split (Template 2) - Header then Split
        frames_split = [
            Frame(0, 250*mm, 210*mm, 47*mm, leftPadding=10*mm, rightPadding=10*mm, topPadding=10*mm, bottomPadding=0, id='header'),
            Frame(0, 0, 130*mm, 250*mm, leftPadding=10*mm, rightPadding=10*mm, topPadding=10*mm, id='main'),
            Frame(130*mm, 0, 80*mm, 250*mm, leftPadding=10*mm, rightPadding=10*mm, topPadding=10*mm, id='sidebar')
        ]
        
        # 3. Sidebar Right (Template 5) - Header then Main/Sidebar
        frames_sidebar_right = [
            Frame(0, 260*mm, 210*mm, 37*mm, leftPadding=10*mm, topPadding=5*mm, id='header'),
            Frame(0, 0, 140*mm, 260*mm, leftPadding=10*mm, rightPadding=10*mm, topPadding=10*mm, id='main'),
            Frame(140*mm, 0, 70*mm, 260*mm, leftPadding=10*mm, rightPadding=10*mm, topPadding=20*mm, id='sidebar')
        ]
        
        # 4. Single Column (Template 3)
        frames_single = [Frame(10*mm, 10*mm, 190*mm, 277*mm, id='main')]

        # 5. Generic FULL PAGE Main Frame (For Page 2+ overflow)
        # Positioned to align with the 'main' column of the first page to maintain visual continuity,
        # or full width if preferred. Let's align with main column.
        
        frames_page2 = frames_single # Default
        if self.template_id in ['template-1', 'template-4', 'template-8', 'template-9', 'template-11', 'template-12']:
            frames_page2 = [Frame(70*mm, 10*mm, 140*mm, 277*mm, leftPadding=10*mm, rightPadding=10*mm, id='main')]
        elif self.template_id == 'template-2':
             frames_page2 = [Frame(10*mm, 10*mm, 130*mm, 277*mm, leftPadding=0, rightPadding=10*mm, id='main')]
        elif self.template_id in ['template-5', 'template-15']:
             frames_page2 = [Frame(10*mm, 10*mm, 140*mm, 277*mm, leftPadding=0, rightPadding=10*mm, id='main')]


        # Register Templates
        templates = []
        
        # First Page Template
        if self.template_id in ['template-1', 'template-4', 'template-8', 'template-9', 'template-11', 'template-12']:
            templates.append(PageTemplate(id='FirstPage', frames=frames_sidebar_left, onPage=self.draw_background))
        elif self.template_id == 'template-2':
            templates.append(PageTemplate(id='FirstPage', frames=frames_split, onPage=self.draw_background))
        elif self.template_id in ['template-5', 'template-15']:
            templates.append(PageTemplate(id='FirstPage', frames=frames_sidebar_right, onPage=self.draw_background))
        else:
            templates.append(PageTemplate(id='FirstPage', frames=frames_single, onPage=self.draw_background))
            
        # Second Page Template (Simple Main Column)
        # Note: onPage=self.draw_background is included to keep the sidebar background if desired,
        # but usually page 2 is cleaner. Let's keep background for consistency for now.
        templates.append(PageTemplate(id='SecondPage', frames=frames_page2, onPage=self.draw_background))
        
        doc.addPageTemplates(templates)
        
        # --- Build Stories ---
        stories = []
        
        name = self.parser.get_section('name')
        title = self.parser.get_section('title')
        contact = self.parser.extract_contact()
        summary = self.parser.get_section(['summary', 'professional_summary'])
        experience = self.parser.get_section(['experience', 'work_experience'])
        education = self.parser.get_section(['education'])
        skills = self.parser.get_section(['skills', 'technical_skills'])
        projects = self.parser.get_section(['projects'])

        # Debug logging
        logger.info(f"PDF Generation - Sections found:")
        logger.info(f"  Name: {name[:50] if name else 'MISSING'}")
        logger.info(f"  Title: {title[:50] if title else 'MISSING'}")
        logger.info(f"  Summary: {len(summary)} chars" if summary else "  Summary: MISSING")
        logger.info(f"  Experience: {len(experience)} chars" if experience else "  Experience: MISSING ⚠️")
        logger.info(f"  Education: {len(education)} chars" if education else "  Education: MISSING")
        logger.info(f"  Skills: {len(skills)} chars" if skills else "  Skills: MISSING")
        logger.info(f"  Projects: {len(projects)} chars" if projects else "  Projects: MISSING ⚠️")
        logger.info(f"  All sections in parser: {list(self.parser.sections.keys())}")

        header_flowables = [
            Paragraph(name, self.styles['NameTitle']),
            Paragraph(title, self.styles['RoleTitle']),
            Spacer(1, 5*mm)
        ]

        if self.template_id in ['template-1', 'template-4', 'template-8', 'template-9', 'template-11', 'template-12']:
            # Layout: Sidebar -> Main
            
            # 1. Sidebar Content
            stories.extend(header_flowables)
            stories.append(Paragraph("CONTACT", self.styles['SidebarHeader']))
            for k, v in contact.items():
                if v: stories.append(Paragraph(v, self.styles['SidebarText']))
            
            if skills:
                stories.append(Paragraph("SKILLS", self.styles['SidebarHeader']))
                stories.extend(self.md_to_flowables(skills, 'SidebarText'))
                
            if education:
                stories.append(Paragraph("EDUCATION", self.styles['SidebarHeader']))
                stories.extend(self.md_to_flowables(education, 'SidebarText'))
            
            # CRITICAL: Switch to SecondPage template for any overflow after this point
            stories.append(NextPageTemplate('SecondPage'))
            stories.append(FrameBreak()) # Jump to Main Frame
            
            # 2. Main Content
            if summary:
                stories.append(Paragraph("PROFESSIONAL PROFILE", self.styles['SectionHeader']))
                stories.extend(self.md_to_flowables(summary, 'MainText'))
            
            if experience:
                stories.append(Paragraph("EXPERIENCE", self.styles['SectionHeader']))
                stories.extend(self.md_to_flowables(experience, 'MainText'))
                
            if projects:
                stories.append(Paragraph("PROJECTS", self.styles['SectionHeader']))
                stories.extend(self.md_to_flowables(projects, 'MainText'))
            
        elif self.template_id in ['template-2', 'template-5', 'template-15']:
             # Layout: Header -> Main -> Sidebar (T2) or Header -> Main -> Sidebar (T5)
             # Wait, T2 frames are [Header, Main, Sidebar].
             # T5 frames are [Header, Main, Sidebar].
             
             # 1. Header
             stories.extend(header_flowables)
             stories.append(FrameBreak()) # To Main
             
             # 2. Main Content
             if summary:
                stories.append(Paragraph("SUMMARY", self.styles['SectionHeader']))
                stories.extend(self.md_to_flowables(summary, 'MainText'))
            
             if experience:
                stories.append(Paragraph("EXPERIENCE", self.styles['SectionHeader']))
                stories.extend(self.md_to_flowables(experience, 'MainText'))
             
             # Before jumping to Sidebar, we must consider page overflow.
             # If Main content was huge, it would have already triggered SecondPage (because Main frame is full).
             # But if we force FrameBreak to go to Sidebar, that's fine for Page 1.
             # Issue: What if Sidebar content is huge? It flows to...?
             # For T2/T5, the Sidebar is frame 2. Page 2 has only 1 frame ('SecondPage' template).
             # If Sidebar overflows, it will go to Page 2 main frame. Accepted.
             
             # But wait, we need to set NextPageTemplate BEFORE filling Main, 
             # so that if Main overflows, it uses SecondPage.
             stories.insert(len(header_flowables) + 1, NextPageTemplate('SecondPage')) 
             # Wait, insert is risky with list logic. Let's reconstruct order.
             
             # Re-doing T2/T5 order:
             stories = []
             stories.extend(header_flowables)
             
             # Set Next Template for overflow
             stories.append(NextPageTemplate('SecondPage'))
             stories.append(FrameBreak()) # To Main
             
             # Main
             if summary:
                stories.append(Paragraph("SUMMARY", self.styles['SectionHeader']))
                stories.extend(self.md_to_flowables(summary, 'MainText'))
            
             if experience:
                stories.append(Paragraph("EXPERIENCE", self.styles['SectionHeader']))
                stories.extend(self.md_to_flowables(experience, 'MainText'))
                
             # Now, we want to put Sidebar content.
             # Problem: If Main overflowed to Page 2, we are now on Page 2 (Template: SecondPage, 1 Frame).
             # We want Sidebar content to appear on Page 1 Sidebar Frame if possible?
             # ReportLab flow is sequential. We can't go "back" to Page 1 Sidebar if we are on Page 2.
             # So Sidebar content MUST come before Main content if we want it guaranteed on Page 1?
             # But the visual layout is Main (Left) Sidebar (Right). Framework fills Frame 0, then 1, then 2.
             # T2 Frames: 0=Header, 1=Main, 2=Sidebar.
             # So we MUST fill Main first. If Main is too long => Page 2. Sidebar content appears on Page 2.
             # This is a limitation of flowable layout.
             # "Fix": Put sidebar content in a Table? Or accept that deep Main content pushes Sidebar to Page 2 (at bottom).
             # Given the "Truncation" issue, the priority is NOT LOSING DATA.
             
             stories.append(FrameBreak()) # To Sidebar (or next page if full)
             
             stories.append(Paragraph("CONTACT", self.styles['SectionHeader']))
             for k, v in contact.items():
                if v: stories.append(Paragraph(v, self.styles['MainText']))
                
             if skills:
                stories.append(Paragraph("SKILLS", self.styles['SectionHeader']))
                stories.extend(self.md_to_flowables(skills, 'MainText'))
                
             if education:
                 stories.append(Paragraph("EDUCATION", self.styles['SectionHeader']))
                 stories.extend(self.md_to_flowables(education, 'MainText'))
                 
        else:
            # Single Column (Template 3)
            # Just flow it.
            stories.append(NextPageTemplate('SecondPage')) # Consistent
            stories.extend(header_flowables)
            # ... (rest of T3 logic same as before)
            contact_line = " | ".join([v for v in contact.values() if v])
            stories.append(Paragraph(contact_line, ParagraphStyle('ContactLine', parent=self.styles['Normal'], alignment=TA_CENTER)))
            stories.append(Spacer(1, 5*mm))
            
            if summary:
                stories.append(Paragraph("PROFILE", self.styles['SectionHeader']))
                stories.extend(self.md_to_flowables(summary, 'MainText'))
            
            if skills:
                stories.append(Paragraph("SKILLS", self.styles['SectionHeader']))
                stories.extend(self.md_to_flowables(skills, 'MainText'))
                
            if experience:
                stories.append(Paragraph("EXPERIENCE", self.styles['SectionHeader']))
                stories.extend(self.md_to_flowables(experience, 'MainText'))
                
            if education:
                 stories.append(Paragraph("EDUCATION", self.styles['SectionHeader']))
                 stories.extend(self.md_to_flowables(education, 'MainText'))

        try:
            doc.build(stories)
            return buffer.getvalue()
        except Exception as e:
            logger.error(f"PDF Build Error: {e}", exc_info=True)
            return b""


def markdown_to_pdf(markdown_text, template_id='modern'):
    try:
        generator = PDFGenerator(markdown_text, template_id)
        return generator.generate()
    except Exception as e:
        logger.error(f"Generation failed: {e}", exc_info=True)
        # Fallback to simple bytes
        return markdown_text.encode('utf-8')
