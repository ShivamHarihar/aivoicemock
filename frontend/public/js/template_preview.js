// Template Preview System with Intelligent Content Mapping
// Parses resume markdown and generates template-specific HTML

class ResumeParser {
    constructor(markdown) {
        this.markdown = markdown;
        this.sections = {};
        this.parse();
    }

    parse() {
        const lines = this.markdown.split('\n');
        let currentSection = null;
        let content = [];

        // Extract name (usually first line with #)
        const nameMatch = this.markdown.match(/^#\s+(.+)/m);
        this.sections.name = nameMatch ? nameMatch[1].trim() : 'Your Name';

        // Extract title/role (usually second line or bold text)
        const titleMatch = this.markdown.match(/\*\*(.+?)\*\*/);
        this.sections.title = titleMatch ? titleMatch[1].trim() : '';

        // Extract contact info (email, phone, location, linkedin)
        this.sections.contact = this.extractContact();

        // Extract sections
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();

            if (line.startsWith('##')) {
                // Save previous section
                if (currentSection && content.length > 0) {
                    this.sections[currentSection] = content.join('\n').trim();
                }

                // Start new section
                currentSection = line.replace(/^##\s+/, '').toLowerCase().replace(/\s+/g, '_');
                content = [];
            } else if (currentSection) {
                content.push(lines[i]);
            }
        }

        // Save last section
        if (currentSection && content.length > 0) {
            this.sections[currentSection] = content.join('\n').trim();
        }
    }

    extractContact() {
        const contact = {};

        // Email
        const emailMatch = this.markdown.match(/([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)/);
        if (emailMatch) contact.email = emailMatch[1];

        // Phone
        const phoneMatch = this.markdown.match(/(\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9})/);
        if (phoneMatch) contact.phone = phoneMatch[1];

        // LinkedIn
        const linkedinMatch = this.markdown.match(/(linkedin\.com\/in\/[^\s)]+)/);
        if (linkedinMatch) contact.linkedin = linkedinMatch[1];

        // Location (common patterns)
        const locationMatch = this.markdown.match(/([A-Z][a-z]+,\s*[A-Z]{2}|[A-Z][a-z]+,\s*[A-Z][a-z]+)/);
        if (locationMatch) contact.location = locationMatch[1];

        return contact;
    }

    getSectionContent(sectionName) {
        const possibleKeys = [
            sectionName,
            sectionName.replace(/_/g, ' '),
            sectionName.toLowerCase(),
            sectionName.toUpperCase()
        ];

        for (const key of possibleKeys) {
            if (this.sections[key]) return this.sections[key];
        }

        // Try partial match
        for (const key in this.sections) {
            if (key.includes(sectionName) || sectionName.includes(key)) {
                return this.sections[key];
            }
        }

        return '';
    }
}

// Template HTML Generators
class TemplateGenerator {
    constructor(parser) {
        this.parser = parser;
    }

    // Generate Generic Template (All new templates use this currently)
    generateGeneric(templateId) {
        const { name, title, contact } = this.parser.sections;
        const summary = this.parser.getSectionContent('summary') || this.parser.getSectionContent('professional_summary') || this.parser.getSectionContent('about');
        const skills = this.parser.getSectionContent('skills') || this.parser.getSectionContent('technical_skills') || this.parser.getSectionContent('core_competencies') || this.parser.getSectionContent('technologies') || this.parser.getSectionContent('tech_stack');
        const experience = this.parser.getSectionContent('experience') || this.parser.getSectionContent('work_experience') || this.parser.getSectionContent('professional_experience') || this.parser.getSectionContent('employment_history');
        const education = this.parser.getSectionContent('education') || this.parser.getSectionContent('academic_background') || this.parser.getSectionContent('qualifications');
        const projects = this.parser.getSectionContent('projects') || this.parser.getSectionContent('key_projects') || this.parser.getSectionContent('personal_projects');
        const certifications = this.parser.getSectionContent('certifications') || this.parser.getSectionContent('certificates') || this.parser.getSectionContent('courses') || this.parser.getSectionContent('training') || this.parser.getSectionContent('licenses');
        const languages = this.parser.getSectionContent('languages');
        const awards = this.parser.getSectionContent('awards') || this.parser.getSectionContent('achievements');

        // Build contact section HTML
        let contactHTML = '';
        if (contact && Object.keys(contact).length > 0) {
            contactHTML = '<div class="section-contact"><h2>Contact</h2><ul>';
            if (contact.email) contactHTML += `<li>📧 ${contact.email}</li>`;
            if (contact.phone) contactHTML += `<li>📱 ${contact.phone}</li>`;
            if (contact.location) contactHTML += `<li>📍 ${contact.location}</li>`;
            if (contact.linkedin) contactHTML += `<li>🔗 ${contact.linkedin}</li>`;
            contactHTML += '</ul></div>';
        }

        // Generic structure matching backend/src/pdf_generator.py and template CSS
        return `
            <div class="resume-container" data-template="${templateId}">
                <div class="resume-header">
                    <h1>${name || 'Your Name'}</h1>
                    ${title ? `<p>${title}</p>` : ''}
                </div>
                
                ${contactHTML}
                ${skills ? `<div class="section-skills"><h2>Skills</h2>${this.markdownToHtml(skills)}</div>` : ''}
                ${languages ? `<div class="section-languages"><h2>Languages</h2>${this.markdownToHtml(languages)}</div>` : ''}
                ${certifications ? `<div class="section-certifications"><h2>Certifications</h2>${this.markdownToHtml(certifications)}</div>` : ''}
                ${awards ? `<div class="section-awards"><h2>Awards</h2>${this.markdownToHtml(awards)}</div>` : ''}
                
                ${summary ? `<div class="section-summary"><h2>Professional Summary</h2>${this.markdownToHtml(summary)}</div>` : ''}
                ${experience ? `<div class="section-experience"><h2>Experience</h2>${this.markdownToHtmlTimeline(experience)}</div>` : ''}
                ${education ? `<div class="section-education"><h2>Education</h2>${this.markdownToHtml(education)}</div>` : ''}
                ${projects ? `<div class="section-projects"><h2>Projects</h2>${this.markdownToHtml(projects)}</div>` : ''}
            </div>
        `;
    }

    markdownToHtml(markdown) {
        if (!markdown) return '';

        let html = markdown
            // Convert headings
            .replace(/^#### (.+)$/gm, '<h4>$1</h4>')
            .replace(/^### (.+)$/gm, '<h3>$1</h3>')
            // Convert bold and italic
            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.+?)\*/g, '<em>$1</em>')
            // Convert lists
            .replace(/^- (.+)$/gm, '<li>$1</li>')
            .replace(/^• (.+)$/gm, '<li>$1</li>')
            .replace(/^\* (.+)$/gm, '<li>$1</li>');

        // Wrap consecutive list items in ul tags
        html = html.replace(/((?:<li>.*?<\/li>\s*)+)/g, '<ul>$1</ul>');

        // Clean up nested ul tags
        html = html.replace(/<\/ul>\s*<ul>/g, '');

        // Convert remaining lines to paragraphs (but not if they're already wrapped)
        html = html.split('\n').map(line => {
            line = line.trim();
            if (!line) return '';
            if (line.startsWith('<')) return line; // Already HTML
            return `<p>${line}</p>`;
        }).join('\n');

        // Clean up empty paragraphs
        html = html.replace(/<p>\s*<\/p>/g, '');

        return html;
    }

    markdownToHtmlTimeline(markdown) {
        if (!markdown) return '';

        // Split by h3 headings (job titles/positions)
        const sections = markdown.split(/(?=###\s)/);

        let html = '';
        sections.forEach(section => {
            if (!section.trim()) return;

            // Extract job title
            const titleMatch = section.match(/^###\s+(.+)$/m);
            const title = titleMatch ? titleMatch[1] : '';

            // Extract company/dates (usually the next line after title)
            const lines = section.split('\n').filter(l => l.trim());
            const companyLine = lines[1] || '';

            // Extract bullet points
            const bullets = section.match(/^[-•*]\s+(.+)$/gm) || [];

            if (title) {
                html += '<div class="experience-item">';
                html += `<h3>${title}</h3>`;
                if (companyLine && !companyLine.startsWith('###')) {
                    html += `<p class="company-info">${companyLine.replace(/^[-•*]\s+/, '')}</p>`;
                }
                if (bullets.length > 0) {
                    html += '<ul>';
                    bullets.forEach(bullet => {
                        const text = bullet.replace(/^[-•*]\s+/, '').replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
                        html += `<li>${text}</li>`;
                    });
                    html += '</ul>';
                }
                html += '</div>';
            }
        });

        return html || this.markdownToHtml(markdown);
    }
}

// Main preview update function
function updatePreviewWithTemplate(templateId) {
    const previewEl = document.getElementById('resume-preview');
    if (!previewEl || !window.recreatedResumeData) return;

    const markdown = window.recreatedResumeData.resume_markdown;
    const parser = new ResumeParser(markdown);
    const generator = new TemplateGenerator(parser);

    let html = '';
    // Use generic generator for all templates (template-1 to template-5)
    // Legacy templates (modern, classic, etc.) have been removed
    html = generator.generateGeneric(templateId);

    previewEl.innerHTML = html;

    // Load template CSS
    loadTemplateCSS(templateId);
}

function loadTemplateCSS(templateId) {
    // Remove existing template stylesheets
    const existingLinks = document.querySelectorAll('link[data-template-css]');
    existingLinks.forEach(link => link.remove());

    // Add new template stylesheet
    const link = document.createElement('link');
    link.rel = 'stylesheet';

    if (templateId.startsWith('template-')) {
        // New structure served via /templates route
        // Add cache buster to force reload
        const ts = new Date().getTime();
        link.href = `/templates/${templateId}/styles.css?v=${ts}`;

        // Also add print.css
        const printLink = document.createElement('link');
        printLink.rel = 'stylesheet';
        printLink.href = `/templates/${templateId}/print.css?v=${ts}`;
        printLink.media = 'print';
        printLink.setAttribute('data-template-css', 'true');
        document.head.appendChild(printLink);
    } else {
        // Legacy structure
        link.href = `/templates/css/${templateId}.css`;
    }

    link.setAttribute('data-template-css', 'true');
    document.head.appendChild(link);
}

// Export for use in ats_dashboard.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ResumeParser, TemplateGenerator, updatePreviewWithTemplate };
}
