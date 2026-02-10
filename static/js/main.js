// Student Attendance System JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips and other interactive elements
    initializeTooltips();
    initializeFormValidation();
    initializeAttendanceForm();
});

// Initialize tooltips
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');
            tooltip.style.cssText = `
                position: absolute;
                background: #1f2937;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 12px;
                z-index: 1000;
                white-space: nowrap;
            `;
            
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
            
            this.tooltip = tooltip;
        });
        
        element.addEventListener('mouseleave', function() {
            if (this.tooltip) {
                this.tooltip.remove();
                this.tooltip = null;
            }
        });
    });
}

// Initialize form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    showError(field, 'This field is required');
                    isValid = false;
                } else {
                    clearError(field);
                }
                
                // Email validation
                if (field.type === 'email' && field.value) {
                    if (!validateEmail(field.value)) {
                        showError(field, 'Please enter a valid email address');
                        isValid = false;
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    });
}

// Initialize attendance form
function initializeAttendanceForm() {
    const attendanceForm = document.getElementById('attendanceForm');
    const saveButton = document.getElementById('saveAttendance');
    
    if (attendanceForm && saveButton) {
        saveButton.addEventListener('click', function() {
            saveAttendance();
        });
    }
    
    // Auto-save functionality
    const checkboxes = document.querySelectorAll('input[type="radio"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            // Show save indicator
            showSaveIndicator();
        });
    });
}

// Save attendance function
async function saveAttendance() {
    const form = document.getElementById('attendanceForm');
    const saveButton = document.getElementById('saveAttendance');
    const originalText = saveButton.textContent;
    
    // Show loading state
    saveButton.innerHTML = '<span class="spinner"></span> Saving...';
    saveButton.disabled = true;
    
    try {
        const formData = new FormData(form);
        const response = await fetch('/save_attendance', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('success', result.message);
            hideSaveIndicator();
        } else {
            showAlert('danger', result.message || 'Error saving attendance');
        }
    } catch (error) {
        showAlert('danger', 'Network error. Please try again.');
        console.error('Error:', error);
    } finally {
        // Reset button state
        saveButton.textContent = originalText;
        saveButton.disabled = false;
    }
}

// Show alert message
function showAlert(type, message) {
    const alertContainer = document.getElementById('alertContainer') || createAlertContainer();
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    
    alertContainer.appendChild(alert);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

// Create alert container if it doesn't exist
function createAlertContainer() {
    const container = document.createElement('div');
    container.id = 'alertContainer';
    container.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        max-width: 400px;
    `;
    document.body.appendChild(container);
    return container;
}

// Show error for form field
function showError(field, message) {
    clearError(field);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
        color: #ef4444;
        font-size: 12px;
        margin-top: 4px;
    `;
    
    field.style.borderColor = '#ef4444';
    field.parentNode.appendChild(errorDiv);
}

// Clear error for form field
function clearError(field) {
    field.style.borderColor = '';
    const errorDiv = field.parentNode.querySelector('.field-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Validate email
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Show save indicator
function showSaveIndicator() {
    const indicator = document.getElementById('saveIndicator') || createSaveIndicator();
    indicator.style.display = 'block';
}

// Hide save indicator
function hideSaveIndicator() {
    const indicator = document.getElementById('saveIndicator');
    if (indicator) {
        indicator.style.display = 'none';
    }
}

// Create save indicator
function createSaveIndicator() {
    const indicator = document.createElement('div');
    indicator.id = 'saveIndicator';
    indicator.textContent = 'You have unsaved changes';
    indicator.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #f59e0b;
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 9998;
        display: none;
    `;
    document.body.appendChild(indicator);
    return indicator;
}

// Date picker functionality
function initializeDatePicker() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    
    dateInputs.forEach(input => {
        // Set max date to today
        input.max = new Date().toISOString().split('T')[0];
        
        // Add change event listener
        input.addEventListener('change', function() {
            const form = this.closest('form');
            if (form) {
                form.submit();
            }
        });
    });
}

// Tab functionality
function initializeTabs() {
    const tabs = document.querySelectorAll('.nav-tab');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetId = this.getAttribute('data-tab');
            
            // Remove active class from all tabs and contents
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            this.classList.add('active');
            const targetContent = document.getElementById(targetId);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });
}

// Export functions for global use
window.showAlert = showAlert;
window.saveAttendance = saveAttendance;
window.initializeDatePicker = initializeDatePicker;
window.initializeTabs = initializeTabs;

// Initialize date picker and tabs when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeDatePicker();
    initializeTabs();
});
