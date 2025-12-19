// ATS Dashboard JavaScript
// Handles data population, animations, and AI recreation

let currentAnalysisData = null;
let currentResumeText = null;

// Initialize dashboard with data from session storage or API
document.addEventListener('DOMContentLoaded', function () {
    loadAnalysisData();

    // Initialize template selection handlers
    setTimeout(() => {
        initializeTemplateSelector();
    }, 500);
});

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

function loadAnalysisData() {
    // Get data from session storage (set by resume_analysis page)
    const dataStr = sessionStorage.getItem('ats_analysis_data');
    const resumeText = sessionStorage.getItem('resume_text');

    if (dataStr) {
        currentAnalysisData = JSON.parse(dataStr);
        currentResumeText = resumeText;
        populateDashboard(currentAnalysisData);
    } else {
        // Fallback: show error or redirect
        console.error('No analysis data found');
        setTimeout(() => {
            window.location.href = '/resume_analysis';
        }, 2000);
    }
}

function populateDashboard(data) {
    // Animate overall ATS score
    animateScore(data.overall_score);

    // Set score tier
    setScoreTier(data.overall_score);

    // Update top stats
    updateTopStats(data);

    // Populate individual metrics
    const factors = data.factor_scores || {};
    animateMetric('keywords', factors.skills || 70);
    animateMetric('skills', factors.skills || 70);
    animateMetric('format', factors.formatting || 70);
    animateMetric('impact', factors.impact || 70);

    // Populate lists
    populateList('strengths-list', data.strengths || [], 'success');
    populateList('improvements-list', data.weaknesses || [], 'warning');
    populateList('recommendations-list', data.career_roadmap || [], 'info');

    // Update list counts
    updateListCounts(data);

    // Update charts if available
    if (typeof updateChartsWithData === 'function') {
        updateChartsWithData(data);
    }

    // Update funnel values
    updateFunnelValues(data);
}

function updateTopStats(data) {
    // Update overall score stat
    const overallScoreStat = document.getElementById('overall-score-stat');
    if (overallScoreStat) {
        animateNumber(overallScoreStat, 0, data.overall_score, 2000);
    }

    // Update match rate
    const matchRateStat = document.getElementById('match-rate-stat');
    if (matchRateStat) {
        const matchRate = data.factor_scores?.skills || 75;
        animateNumber(matchRateStat, 0, matchRate, 2000, '%');
    }

    // Update optimization level
    const optimizationStat = document.getElementById('optimization-stat');
    if (optimizationStat) {
        const score = data.overall_score;
        optimizationStat.textContent = score >= 80 ? 'High' : score >= 60 ? 'Medium' : 'Low';
    }

    // Update ranking
    const rankingStat = document.getElementById('ranking-stat');
    if (rankingStat) {
        const score = data.overall_score;
        rankingStat.textContent = score >= 90 ? 'Top 5%' : score >= 80 ? 'Top 10%' : score >= 70 ? 'Top 25%' : 'Top 50%';
    }
}

function updateListCounts(data) {
    const strengthsCount = document.getElementById('strengths-count');
    if (strengthsCount) {
        strengthsCount.textContent = (data.strengths || []).length;
    }

    const improvementsCount = document.getElementById('improvements-count');
    if (improvementsCount) {
        improvementsCount.textContent = (data.weaknesses || []).length;
    }

    const recommendationsCount = document.getElementById('recommendations-count');
    if (recommendationsCount) {
        recommendationsCount.textContent = (data.career_roadmap || []).length;
    }
}

function updateFunnelValues(data) {
    const factors = data.factor_scores || {};

    const funnelContent = document.getElementById('funnel-content');
    if (funnelContent) funnelContent.textContent = (factors.impact || 95) + '%';

    const funnelKeywords = document.getElementById('funnel-keywords');
    if (funnelKeywords) funnelKeywords.textContent = (factors.skills || 85) + '%';

    const funnelFormat = document.getElementById('funnel-format');
    if (funnelFormat) funnelFormat.textContent = (factors.formatting || 70) + '%';

    const funnelAts = document.getElementById('funnel-ats');
    if (funnelAts) funnelAts.textContent = data.overall_score + '%';
}

function animateNumber(element, start, end, duration, suffix = '') {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.round(current) + suffix;
    }, 16);
}


function animateScore(targetScore) {
    const scoreDisplay = document.getElementById('ats-score-display');
    const scoreCircle = document.getElementById('ats-score-circle');
    const circumference = 2 * Math.PI * 90; // r = 90

    let currentScore = 0;
    const duration = 2000; // 2 seconds
    const steps = 60;
    const increment = targetScore / steps;
    const stepDuration = duration / steps;

    const interval = setInterval(() => {
        currentScore += increment;
        if (currentScore >= targetScore) {
            currentScore = targetScore;
            clearInterval(interval);
        }

        // Update number
        scoreDisplay.textContent = Math.round(currentScore);

        // Update circle
        const offset = circumference - (currentScore / 100) * circumference;
        scoreCircle.style.strokeDasharray = `${circumference} ${circumference}`;
        scoreCircle.style.strokeDashoffset = offset;
    }, stepDuration);
}

function setScoreTier(score) {
    const titleEl = document.getElementById('score-title');
    const descEl = document.getElementById('score-description');
    const tierEl = document.getElementById('score-tier');

    let tier, title, description, color;

    if (score >= 80) {
        tier = 'Excellent';
        title = 'Outstanding Resume! 🎉';
        description = 'Your resume is highly optimized for ATS systems';
        color = '#10b981'; // green
    } else if (score >= 60) {
        tier = 'Good';
        title = 'Good Resume 👍';
        description = 'Your resume meets most ATS requirements';
        color = '#f59e0b'; // yellow
    } else {
        tier = 'Needs Improvement';
        title = 'Room for Improvement 📝';
        description = 'Your resume could benefit from optimization';
        color = '#ef4444'; // red
    }

    titleEl.textContent = title;
    descEl.textContent = description;
    tierEl.innerHTML = `<span class="tier-badge" style="background: ${color}">${tier}</span>`;
}

function animateMetric(metricName, targetValue) {
    const valueEl = document.getElementById(`${metricName}-score`);
    const barEl = document.getElementById(`${metricName}-bar`);

    let currentValue = 0;
    const duration = 1500;
    const steps = 50;
    const increment = targetValue / steps;
    const stepDuration = duration / steps;

    setTimeout(() => {
        const interval = setInterval(() => {
            currentValue += increment;
            if (currentValue >= targetValue) {
                currentValue = targetValue;
                clearInterval(interval);
            }

            valueEl.textContent = Math.round(currentValue);
            barEl.style.width = currentValue + '%';

            // Color based on score
            if (currentValue >= 80) {
                barEl.style.background = 'linear-gradient(90deg, #10b981, #059669)';
            } else if (currentValue >= 60) {
                barEl.style.background = 'linear-gradient(90deg, #f59e0b, #d97706)';
            } else {
                barEl.style.background = 'linear-gradient(90deg, #ef4444, #dc2626)';
            }
        }, stepDuration);
    }, 300); // Delay start
}

function populateList(listId, items, type) {
    const listEl = document.getElementById(listId);
    listEl.innerHTML = '';

    if (items.length === 0) {
        listEl.innerHTML = '<li class="empty-item">No items to display</li>';
        return;
    }

    items.forEach((item, index) => {
        const li = document.createElement('li');
        li.textContent = item;
        li.style.animationDelay = `${index * 0.1}s`;
        li.classList.add('fade-in-item');
        listEl.appendChild(li);
    });
}

// AI Resume Recreation
async function recreateResumeWithAI() {
    const btn = document.getElementById('recreate-btn');
    const originalHTML = btn.innerHTML;

    // Show loading state
    btn.innerHTML = '<div class="spinner"></div> <span>AI is recreating your resume...</span>';
    btn.disabled = true;

    try {
        const response = await fetch('/api/recreate_resume', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                resume_text: currentResumeText,
                current_score: currentAnalysisData.overall_score,
                analysis: currentAnalysisData
            })
        });

        const result = await response.json();

        if (result.error) {
            alert('Error: ' + result.error);
            btn.innerHTML = originalHTML;
            btn.disabled = false;
            return;
        }

        // Save to session storage
        sessionStorage.setItem('recreated_resume_content', JSON.stringify(result));

        // Success state
        btn.innerHTML = '✅ Resume Recreated Successfully!';

        // Redirect to new page
        setTimeout(() => {
            window.location.href = '/recreate_resume_page';
        }, 1000);

    } catch (error) {
        console.error('Recreation failed:', error);
        alert('Failed to recreate resume. Please try again.');
        btn.innerHTML = originalHTML;
        btn.disabled = false;
    }
}

function displayRecreatedResume(result) {
    const section = document.getElementById('recreated-section');
    section.style.display = 'block';

    // Update scores
    document.getElementById('old-score').textContent = result.old_score;
    document.getElementById('new-score').textContent = result.new_score;

    const improvement = result.new_score - result.old_score;
    const improvementBadge = document.getElementById('improvement-badge');

    // Special handling for already optimized resumes
    if (result.already_optimized) {
        improvementBadge.textContent = '+0%';
        improvementBadge.style.background = '#3b82f6'; // blue for info

        // Show friendly message
        const messageDiv = document.createElement('div');
        messageDiv.style.cssText = 'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: center;';
        messageDiv.innerHTML = `
            <h3 style="margin: 0 0 10px 0; font-size: 1.2rem;">🎉 Great News!</h3>
            <p style="margin: 0; opacity: 0.95;">${result.message}</p>
        `;
        section.insertBefore(messageDiv, section.firstChild);
    } else {
        improvementBadge.textContent = improvement > 0 ? `+${improvement}%` : `${improvement}%`;
        improvementBadge.style.background = improvement > 0 ? '#10b981' : '#ef4444';
    }

    // Display resume content
    document.getElementById('resume-preview').innerHTML = '<div class="preview-loading">Loading preview...</div>';
    document.getElementById('resume-markdown').textContent = result.resume_markdown;

    // Store for download
    window.recreatedResumeData = result;

    // Initialize preview with default template (modern)
    setTimeout(() => {
        if (typeof updatePreviewWithTemplate === 'function') {
            updatePreviewWithTemplate('template-1');
        } else {
            // Fallback to simple markdown display
            document.getElementById('resume-preview').innerHTML = marked(result.resume_markdown);
        }
    }, 100);
}

function showFormat(format) {
    // Remove active class from all tabs and content
    document.querySelectorAll('.format-tab').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.format-content').forEach(content => content.classList.remove('active'));

    // Add active class to selected
    event.target.classList.add('active');
    document.getElementById(`${format}-content`).classList.add('active');
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

        // Get original filename from session storage
        let originalFilename = sessionStorage.getItem('original_filename') || 'resume';
        // Remove extension if present
        originalFilename = originalFilename.replace(/\.[^/.]+$/, '');

        // Call backend to generate PDF
        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = '⏳ Generating PDF...';
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
                    // Try to get error message from JSON
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
                alert(`Failed to generate PDF: ${error.message}\n\nPlease try downloading as Markdown instead.`);
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

        // Get original filename
        let originalFilename = sessionStorage.getItem('original_filename') || 'resume';
        originalFilename = originalFilename.replace(/\.[^/.]+$/, '');

        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = '⏳ Generating DOCX...';
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


function copyToClipboard() {
    if (!window.recreatedResumeData) {
        alert('No recreated resume available');
        return;
    }

    const markdown = window.recreatedResumeData.resume_markdown;
    navigator.clipboard.writeText(markdown).then(() => {
        alert('Resume copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// Simple markdown renderer (fallback if marked.js not available)
function marked(markdown) {
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
