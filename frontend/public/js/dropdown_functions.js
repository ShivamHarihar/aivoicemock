// Dropdown toggle for download options
function toggleDownloadDropdown(event) {
    event.stopPropagation();
    const dropdown = document.getElementById('download-dropdown');
    if (dropdown.style.display === 'none' || dropdown.style.display === '') {
        dropdown.style.display = 'block';
    } else {
        dropdown.style.display = 'none';
    }
}

function hideDownloadDropdown() {
    const dropdown = document.getElementById('download-dropdown');
    if (dropdown) {
        dropdown.style.display = 'none';
    }
}

// Close dropdown when clicking outside
document.addEventListener('click', function (event) {
    const dropdown = document.getElementById('download-dropdown');
    const btn = document.getElementById('download-dropdown-btn');
    if (dropdown && btn && !btn.contains(event.target) && !dropdown.contains(event.target)) {
        dropdown.style.display = 'none';
    }
});
