// JavaScript for Attendance System
// Function to initialize camera controls
function initializeCameraControls() {
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const videoFeed = document.getElementById('videoFeed');

    if (startBtn && stopBtn && videoFeed) {
        startBtn.addEventListener('click', function() {
            fetch('/start_camera')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'started') {
                        videoFeed.src = '/video_feed';
                        this.disabled = true;
                        stopBtn.disabled = false;
                    }
                });
        });

        stopBtn.addEventListener('click', function() {
            fetch('/stop_camera')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'stopped') {
                        videoFeed.src = '';
                        this.disabled = true;
                        startBtn.disabled = false;
                    }
                });
        });
    }
}

// Function to handle form validation
function setupFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = this.querySelectorAll('input[required]');
            let valid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    valid = false;
                    highlightField(input, false);
                } else {
                    highlightField(input, true);
                }
            });
            
            if (!valid) {
                e.preventDefault();
                showToast('Please fill in all required fields', 'error');
            }
        });
    });
}

// Helper function to highlight form fields
function highlightField(field, isValid) {
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
    }
}

// Toast notification system
function showToast(message, type = 'info') {
    // Remove any existing toasts
    const existingToasts = document.querySelectorAll('.custom-toast');
    existingToasts.forEach(toast => toast.remove());
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `custom-toast alert alert-${type} alert-dismissible fade show`;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 250px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.remove();
        }
    }, 5000);
}

// Date picker initialization for reports page
function initializeDatePicker() {
    const dateInput = document.getElementById('date');
    
    if (dateInput) {
        // Set default to today if no value
        if (!dateInput.value) {
            const today = new Date();
            dateInput.value = today.toISOString().split('T')[0];
        }
        
        // Add change event listener
        dateInput.addEventListener('change', function() {
            this.closest('form').submit();
        });
    }
}

// Table sorting functionality for reports
function initializeTableSorting() {
    const table = document.querySelector('table');
    
    if (table) {
        const headers = table.querySelectorAll('th');
        
        headers.forEach((header, index) => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => {
                sortTable(index);
            });
        });
    }
}

function sortTable(columnIndex) {
    const table = document.querySelector('table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const isAscending = table.getAttribute('data-sort-direction') === 'asc';
    
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();
        
        // Try to compare as numbers if possible
        if (!isNaN(aValue) && !isNaN(bValue)) {
            return isAscending ? aValue - bValue : bValue - aValue;
        }
        
        // Otherwise compare as strings
        return isAscending 
            ? aValue.localeCompare(bValue)
            : bValue.localeCompare(aValue);
    });
    
    // Remove existing rows
    while (tbody.firstChild) {
        tbody.removeChild(tbody.firstChild);
    }
    
    // Add sorted rows
    rows.forEach(row => tbody.appendChild(row));
    
    // Toggle sort direction
    table.setAttribute('data-sort-direction', isAscending ? 'desc' : 'asc');
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeCameraControls();
    setupFormValidation();
    initializeDatePicker();
    initializeTableSorting();
    
    // Add any other initialization functions here
});

// Export functions for potential modular use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeCameraControls,
        setupFormValidation,
        initializeDatePicker,
        initializeTableSorting,
        showToast
    };
}