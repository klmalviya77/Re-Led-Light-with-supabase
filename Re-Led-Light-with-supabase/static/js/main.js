// Main JavaScript file for Re Led Light website

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
    initializeHoverEffects();
    hidePageLoader();
});

// Hide page loader after content loads
function hidePageLoader() {
    const loader = document.getElementById('pageLoader');
    if (loader) {
        setTimeout(() => {
            loader.classList.add('fade-out');
            setTimeout(() => {
                loader.style.display = 'none';
            }, 300);
        }, 500);
    }
}

// Update cart count in navigation
function updateCartCount() {
    const cart = getCart();
    const cartCount = document.getElementById('cart-count');
    if (cartCount) {
        cartCount.textContent = cart.length;
    }
}

// Get cart from localStorage
function getCart() {
    const cart = localStorage.getItem('cart');
    return cart ? JSON.parse(cart) : [];
}

// Add product to cart
function addToCart(id, name, price, image) {
    const cart = getCart();
    const product = {
        id: id,
        name: name,
        price: price,
        image: image
    };
    
    cart.push(product);
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
}

// Initialize hover effects for cards
function initializeHoverEffects() {
    const hoverCards = document.querySelectorAll('.hover-card');
    hoverCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Smooth scrolling for anchor links
function smoothScroll(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Format price with currency (Indian Rupees)
function formatPrice(price) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(price);
}

// Show loading spinner
function showLoading(element) {
    const spinner = document.createElement('div');
    spinner.className = 'text-center py-3';
    spinner.innerHTML = '<i class="fas fa-spinner fa-spin fa-2x"></i>';
    element.appendChild(spinner);
    return spinner;
}

// Hide loading spinner
function hideLoading(spinner) {
    if (spinner && spinner.parentNode) {
        spinner.parentNode.removeChild(spinner);
    }
}

// Show success message
function showSuccessMessage(message, duration = 3000) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success alert-dismissible fade show position-fixed';
    alert.style.top = '20px';
    alert.style.right = '20px';
    alert.style.zIndex = '9999';
    alert.style.minWidth = '300px';
    
    alert.innerHTML = `
        <i class="fas fa-check-circle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alert);
    
    // Auto dismiss after duration
    setTimeout(() => {
        if (alert.parentNode) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, duration);
}

// Show error message
function showErrorMessage(message, duration = 5000) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show position-fixed';
    alert.style.top = '20px';
    alert.style.right = '20px';
    alert.style.zIndex = '9999';
    alert.style.minWidth = '300px';
    
    alert.innerHTML = `
        <i class="fas fa-exclamation-circle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alert);
    
    // Auto dismiss after duration
    setTimeout(() => {
        if (alert.parentNode) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, duration);
}

// Validate email format
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Validate phone number format
function isValidPhone(phone) {
    const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
    return phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ''));
}

// Format phone number for display
function formatPhone(phone) {
    const cleaned = phone.replace(/\D/g, '');
    const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
    if (match) {
        return `(${match[1]}) ${match[2]}-${match[3]}`;
    }
    return phone;
}

// Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Lazy load images
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Initialize tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize popovers
function initializePopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Handle form submissions with loading states
function handleFormSubmission(form, submitButton, onSubmit) {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const originalText = submitButton.innerHTML;
        submitButton.disabled = true;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        
        onSubmit()
            .then(() => {
                showSuccessMessage('Operation completed successfully!');
            })
            .catch((error) => {
                showErrorMessage(error.message || 'An error occurred');
            })
            .finally(() => {
                submitButton.disabled = false;
                submitButton.innerHTML = originalText;
            });
    });
}

// Initialize all interactive elements
function initializeInteractiveElements() {
    initializeLazyLoading();
    initializeTooltips();
    initializePopovers();
}

// Call initialization when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeInteractiveElements);
} else {
    initializeInteractiveElements();
}
