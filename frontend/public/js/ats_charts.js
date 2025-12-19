// ATS Dashboard Charts
// Initialize all charts and visualizations

let skillsChart, metricsChart, priorityChart;

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function () {
    // Wait for data to load
    setTimeout(() => {
        initializeCharts();
    }, 1000);
});

function initializeCharts() {
    initSkillsChart();
    initMetricsChart();
    initPriorityChart();
}

// Skills Distribution Donut Chart with Center Percentage
function initSkillsChart() {
    const ctx = document.getElementById('skillsChart');
    if (!ctx) return;

    const data = {
        labels: ['Technical Skills', 'Soft Skills', 'Industry Knowledge', 'Tools & Technologies'],
        datasets: [{
            data: [35, 25, 20, 20],
            backgroundColor: [
                'rgba(99, 102, 241, 0.85)',
                'rgba(16, 185, 129, 0.85)',
                'rgba(236, 72, 153, 0.85)',
                'rgba(251, 146, 60, 0.85)'
            ],
            borderColor: [
                'rgb(99, 102, 241)',
                'rgb(16, 185, 129)',
                'rgb(236, 72, 153)',
                'rgb(251, 146, 60)'
            ],
            borderWidth: 3,
            hoverOffset: 12
        }]
    };

    const config = {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 12,
                        font: {
                            family: "'Inter', sans-serif",
                            size: 11,
                            weight: '600'
                        },
                        usePointStyle: true,
                        pointStyle: 'circle',
                        generateLabels: function (chart) {
                            const data = chart.data;
                            if (data.labels.length && data.datasets.length) {
                                return data.labels.map((label, i) => {
                                    const value = data.datasets[0].data[i];
                                    return {
                                        text: `${label}: ${value}%`,
                                        fillStyle: data.datasets[0].backgroundColor[i],
                                        strokeStyle: data.datasets[0].borderColor[i],
                                        lineWidth: 2,
                                        hidden: false,
                                        index: i
                                    };
                                });
                            }
                            return [];
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.9)',
                    padding: 14,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    borderColor: 'rgba(255, 255, 255, 0.2)',
                    borderWidth: 1,
                    callbacks: {
                        label: function (context) {
                            return context.label + ': ' + context.parsed + '%';
                        }
                    }
                }
            },
            cutout: '70%',
            animation: {
                animateRotate: true,
                animateScale: true,
                duration: 1500,
                easing: 'easeInOutQuart'
            }
        }
    };

    skillsChart = new Chart(ctx, config);
}

// Performance Metrics Bar Chart
function initMetricsChart() {
    const ctx = document.getElementById('metricsChart');
    if (!ctx) return;

    const data = {
        labels: ['Keywords', 'Skills', 'Format', 'Experience', 'Education', 'Impact'],
        datasets: [{
            label: 'Score',
            data: [85, 90, 75, 80, 88, 82],
            backgroundColor: [
                'rgba(99, 102, 241, 0.8)',
                'rgba(16, 185, 129, 0.8)',
                'rgba(139, 92, 246, 0.8)',
                'rgba(236, 72, 153, 0.8)',
                'rgba(59, 130, 246, 0.8)',
                'rgba(251, 146, 60, 0.8)'
            ],
            borderColor: [
                'rgb(99, 102, 241)',
                'rgb(16, 185, 129)',
                'rgb(139, 92, 246)',
                'rgb(236, 72, 153)',
                'rgb(59, 130, 246)',
                'rgb(251, 146, 60)'
            ],
            borderWidth: 2,
            borderRadius: 8,
            borderSkipped: false
        }]
    };

    const config = {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 1,
                    callbacks: {
                        label: function (context) {
                            return 'Score: ' + context.parsed.y + '%';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function (value) {
                            return value + '%';
                        },
                        font: {
                            family: "'Inter', sans-serif",
                            size: 11
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)',
                        drawBorder: false
                    }
                },
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        font: {
                            family: "'Inter', sans-serif",
                            size: 11
                        }
                    }
                }
            },
            animation: {
                duration: 1500,
                easing: 'easeInOutQuart'
            }
        }
    };

    metricsChart = new Chart(ctx, config);
}

// Improvement Priority Horizontal Bar Chart
function initPriorityChart() {
    const ctx = document.getElementById('priorityChart');
    if (!ctx) return;

    const data = {
        labels: ['Add Keywords', 'Improve Format', 'Quantify Achievements', 'Update Skills', 'Enhance Summary'],
        datasets: [{
            label: 'Priority Score',
            data: [95, 85, 80, 75, 70],
            backgroundColor: [
                'rgba(239, 68, 68, 0.8)',
                'rgba(251, 146, 60, 0.8)',
                'rgba(251, 191, 36, 0.8)',
                'rgba(16, 185, 129, 0.8)',
                'rgba(59, 130, 246, 0.8)'
            ],
            borderColor: [
                'rgb(239, 68, 68)',
                'rgb(251, 146, 60)',
                'rgb(251, 191, 36)',
                'rgb(16, 185, 129)',
                'rgb(59, 130, 246)'
            ],
            borderWidth: 2,
            borderRadius: 6,
            borderSkipped: false
        }]
    };

    const config = {
        type: 'bar',
        data: data,
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 1,
                    callbacks: {
                        label: function (context) {
                            return 'Priority: ' + context.parsed.x + '/100';
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function (value) {
                            return value;
                        },
                        font: {
                            family: "'Inter', sans-serif",
                            size: 11
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)',
                        drawBorder: false
                    }
                },
                y: {
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        font: {
                            family: "'Inter', sans-serif",
                            size: 11
                        }
                    }
                }
            },
            animation: {
                duration: 1500,
                easing: 'easeInOutQuart'
            }
        }
    };

    priorityChart = new Chart(ctx, config);
}

// Update charts with real data
function updateChartsWithData(analysisData) {
    if (!analysisData) return;

    // Update skills chart if we have skill data
    if (skillsChart && analysisData.skills_breakdown) {
        const skills = analysisData.skills_breakdown;
        skillsChart.data.datasets[0].data = [
            skills.technical || 35,
            skills.soft || 25,
            skills.industry || 20,
            skills.tools || 20
        ];
        skillsChart.update();
    }

    // Update metrics chart
    if (metricsChart && analysisData.factor_scores) {
        const scores = analysisData.factor_scores;
        metricsChart.data.datasets[0].data = [
            scores.keywords || 85,
            scores.skills || 90,
            scores.formatting || 75,
            scores.experience || 80,
            scores.education || 88,
            scores.impact || 82
        ];
        metricsChart.update();
    }

    // Update priority chart based on weaknesses
    if (priorityChart && analysisData.weaknesses) {
        // Calculate priorities based on weaknesses
        const priorities = calculatePriorities(analysisData);
        priorityChart.data.labels = priorities.labels;
        priorityChart.data.datasets[0].data = priorities.scores;
        priorityChart.update();
    }
}

// Calculate improvement priorities
function calculatePriorities(data) {
    const priorities = {
        labels: [],
        scores: []
    };

    // Default priorities
    const defaultPriorities = [
        { label: 'Add Keywords', score: 95 },
        { label: 'Improve Format', score: 85 },
        { label: 'Quantify Achievements', score: 80 },
        { label: 'Update Skills', score: 75 },
        { label: 'Enhance Summary', score: 70 }
    ];

    // Use default for now, can be enhanced with real data
    defaultPriorities.forEach(p => {
        priorities.labels.push(p.label);
        priorities.scores.push(p.score);
    });

    return priorities;
}

// Export for use in main dashboard script
window.updateChartsWithData = updateChartsWithData;
