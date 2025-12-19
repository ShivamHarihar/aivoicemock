// Recreation Resume Page JavaScript
// Handles displaying the recreated resume, template switching, and downloading

document.addEventListener('DOMContentLoaded', function () {
    loadRecreatedResume();
    initializeTemplateSelector();
});

function loadRecreatedResume() {
    // Get data from session storage
    const dataStr = sessionStorage.getItem('recreated_resume_content');

    if (!dataStr) {
        // No data found, redirect back to dashboard
        console.error('No recreated resume data found');
        alert('No resume data found. Redirecting to dashboard...');
        window.location.href = '/ats_dashboard';
        return;
    }

    const result = JSON.parse(dataStr);
    window.recreatedResumeData = result; // Store for other functions

    // Display stats
    document.getElementById('old-score').textContent = result.old_score || 0;
    document.getElementById('new-score').textContent = result.new_score || 0;

    const improvement = (result.new_score || 0) - (result.old_score || 0);
    const improvementBadge = document.getElementById('improvement-badge');

    if (result.already_optimized) {
        improvementBadge.textContent = '+0%';
        improvementBadge.style.background = '#3b82f6';

        // Add message if not exists
        const section = document.querySelector('.glass-panel');
        // We could add the special message here if we want, similar to dashboard
    } else {
        improvementBadge.textContent = improvement > 0 ? `+${improvement}%` : `${improvement}%`;
        improvementBadge.style.background = improvement > 0 ? '#10b981' : '#ef4444';
    }

    // Display content
    document.getElementById('resume-preview').innerHTML = '<div class="preview-loading">Loading preview...</div>';
    document.getElementById('resume-markdown').textContent = result.resume_markdown;

    // Initialize preview with default template
    setTimeout(() => {
        if (typeof updatePreviewWithTemplate === 'function') {
            updatePreviewWithTemplate('template-1');
        } else {
            console.error('updatePreviewWithTemplate function missing');
            document.getElementById('resume-preview').innerHTML = marked(result.resume_markdown);
        }
    }, 100);
}

function initializeTemplateSelector() {
    const templateRadios = document.querySelectorAll('input[name="resume-template"]');

    templateRadios.forEach(radio => {
        radio.addEventListener('change', function () {
            if (this.checked && window.recreatedResumeData) {
                // Update preview with selected template
                updatePreviewWithTemplate(this.value);
            }
        });
    });
}

function showFormat(format) {
    // Remove active class from all tabs and content
    document.querySelectorAll('.format-tab').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.format-content').forEach(content => content.classList.remove('active'));

    // Add active class to selected
    // Note: event might not be defined if called programmatically, but here it is called from onclick
    event.target.classList.add('active');

    // Determine content id
    let contentId = format === 'preview' ? 'preview-content' : 'markdown-content';
    document.getElementById(contentId).classList.add('active');
}

function downloadResume(format) {
    if (!window.recreatedResumeData) {
        alert('No recreated resume available');
        return;
    }

    const data = window.recreatedResumeData;

    if (format === 'markdown') {
        const blob = new Blob([data.resume_markdown], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'optimized_resume.md';
        a.click();
        URL.revokeObjectURL(url);
    } else if (format === 'pdf') {
        // Get selected template
        const templateRadios = document.querySelectorAll('input[name="resume-template"]');
        let selectedTemplate = 'template-1';
        for (const radio of templateRadios) {
            if (radio.checked) {
                selectedTemplate = radio.value;
                break;
            }
        }

        // Get original filename
        let originalFilename = sessionStorage.getItem('original_filename') || 'resume';
        originalFilename = originalFilename.replace(/\.[^/.]+$/, '');

        const btn = event.target;
        const originalText = btn.textContent;
        // Don't change text if it's the dropdown item, might look weird. 
        // But for feedback it is good.
        btn.textContent = '⏳ Generating...';
        btn.disabled = true;

        fetch('/api/download_resume_pdf', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                markdown_text: data.resume_markdown,
                template_id: selectedTemplate
            })
        })
            .then(async response => {
                if (!response.ok) {
                    try {
                        const errorData = await response.json();
                        throw new Error(errorData.error || 'PDF generation failed');
                    } catch (e) {
                        throw new Error('PDF generation failed');
                    }
                }
                return response.blob();
            })
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${originalFilename}_enhanced.pdf`;
                a.click();
                URL.revokeObjectURL(url);
                btn.textContent = originalText;
                btn.disabled = false;
            })
            .catch(error => {
                console.error('PDF download failed:', error);
                alert(`Failed to generate PDF: ${error.message}`);
                btn.textContent = originalText;
                btn.disabled = false;
            });
    } else if (format === 'docx') {
        // Get selected template
        const templateRadios = document.querySelectorAll('input[name="resume-template"]');
        let selectedTemplate = 'template-1';
        for (const radio of templateRadios) {
            if (radio.checked) {
                selectedTemplate = radio.value;
                break;
            }
        }

        let originalFilename = sessionStorage.getItem('original_filename') || 'resume';
        originalFilename = originalFilename.replace(/\.[^/.]+$/, '');

        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = '⏳ Generating...';
        btn.disabled = true;

        fetch('/api/download_resume_docx', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                markdown_text: data.resume_markdown,
                template_id: selectedTemplate
            })
        })
            .then(async response => {
                if (!response.ok) throw new Error('DOCX generation failed');
                return response.blob();
            })
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${originalFilename}_enhanced.docx`;
                a.click();
                URL.revokeObjectURL(url);
                btn.textContent = originalText;
                btn.disabled = false;
            })
            .catch(error => {
                console.error('DOCX download failed:', error);
                alert(`Failed to generate DOCX: ${error.message}`);
                btn.textContent = originalText;
                btn.disabled = false;
            });
    }
}

// Helper for marked (copied from ats_dashboard.js just in case)
function marked(markdown) {
    if (window.marked && typeof window.marked === 'function') return window.marked(markdown);

    return markdown
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
        .replace(/\*(.*)\*/gim, '<em>$1</em>')
        .replace(/\n\n/g, '</p><p>')
        .replace(/^\- (.*$)/gim, '<li>$1</li>')
        .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
        .replace(/^(.+)$/gim, '<p>$1</p>');
}
