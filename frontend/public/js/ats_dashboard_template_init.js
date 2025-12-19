// ATS Dashboard JavaScript
// Handles data population, animations, and AI recreation

let currentAnalysisData = null;
let currentResumeText = null;
let selectedTemplate = 'template-1'; // Default template

// Initialize dashboard with data from session storage or API
document.addEventListener('DOMContentLoaded', function () {
    loadAnalysisData();

    // Add template selection event listeners
    setTimeout(() => {
        const templateRadios = document.querySelectorAll('input[name="resume-template"]');
        templateRadios.forEach(radio => {
            radio.addEventListener('change', function () {
                // Remove highlight from all template cards
                const allCards = document.querySelectorAll('.template-card');
                allCards.forEach(card => {
                    card.style.border = '2px solid rgba(255,255,255,0.1)';
                    card.style.background = 'rgba(255,255,255,0.03)';
                });

                // Highlight selected template card
                const selectedCard = this.nextElementSibling;
                if (selectedCard && selectedCard.classList.contains('template-card')) {
                    selectedCard.style.border = '2px solid rgba(99, 102, 241, 0.3)';
                    selectedCard.style.background = 'rgba(99, 102, 241, 0.1)';
                }
            });
        });
    }, 500);
});
