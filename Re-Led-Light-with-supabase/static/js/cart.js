// Shopping cart functionality for Re Led Light website

// Initialize cart functionality
document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
});

// Get cart items from localStorage
function getCart() {
    const cart = localStorage.getItem('cart');
    return cart ? JSON.parse(cart) : [];
}

// Save cart to localStorage
function saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
}

// Add item to cart
function addToCart(id, name, price, image) {
    const cart = getCart();
    const item = {
        id: parseInt(id),
        name: name,
        price: parseFloat(price),
        image: image,
        timestamp: Date.now()
    };
    
    cart.push(item);
    saveCart(cart);
    
    // Show success feedback
    showCartSuccessMessage(`${name} added to cart!`);
}

// Remove item from cart by ID
function removeFromCart(productId) {
    const cart = getCart();
    const updatedCart = cart.filter(item => item.id !== parseInt(productId));
    saveCart(updatedCart);
}

// Remove all instances of a product from cart
function removeAllFromCart(productId) {
    removeFromCart(productId);
}

// Update item quantity in cart
function updateCartItemQuantity(productId, newQuantity) {
    const cart = getCart();
    const productCart = cart.filter(item => item.id === parseInt(productId));
    const otherItems = cart.filter(item => item.id !== parseInt(productId));
    
    if (newQuantity <= 0) {
        saveCart(otherItems);
        return;
    }
    
    // Adjust quantity by adding/removing items
    const currentQuantity = productCart.length;
    const difference = newQuantity - currentQuantity;
    
    if (difference > 0) {
        // Add more items
        const sampleItem = productCart[0];
        for (let i = 0; i < difference; i++) {
            otherItems.push({ ...sampleItem, timestamp: Date.now() + i });
        }
    } else if (difference < 0) {
        // Remove items
        productCart.splice(0, Math.abs(difference));
        otherItems.push(...productCart);
    }
    
    saveCart(otherItems);
}

// Get cart item count
function getCartItemCount() {
    return getCart().length;
}

// Get unique products in cart with quantities
function getCartSummary() {
    const cart = getCart();
    const summary = {};
    
    cart.forEach(item => {
        if (summary[item.id]) {
            summary[item.id].quantity++;
        } else {
            summary[item.id] = {
                ...item,
                quantity: 1
            };
        }
    });
    
    return Object.values(summary);
}

// Calculate cart total
function getCartTotal() {
    const cart = getCart();
    return cart.reduce((total, item) => total + item.price, 0);
}

// Clear entire cart
function clearCart() {
    localStorage.removeItem('cart');
    updateCartCount();
}

// Update cart count in navigation
function updateCartCount() {
    const cartCount = document.getElementById('cart-count');
    if (cartCount) {
        cartCount.textContent = getCartItemCount();
    }
}

// Show cart success message
function showCartSuccessMessage(message) {
    // Create toast notification
    const toastContainer = getOrCreateToastContainer();
    
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="toast-header">
            <i class="fas fa-shopping-cart text-success me-2"></i>
            <strong class="me-auto">Cart Updated</strong>
            <small>Just now</small>
            <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: 3000
    });
    
    bsToast.show();
    
    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    });
}

// Get or create toast container
function getOrCreateToastContainer() {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    return container;
}

// Mini cart widget (can be used in header)
function createMiniCartWidget() {
    const cart = getCartSummary();
    const total = getCartTotal();
    
    if (cart.length === 0) {
        return `
            <div class="text-center p-3">
                <i class="fas fa-shopping-cart fa-2x text-muted mb-2"></i>
                <p class="text-muted mb-0">Your cart is empty</p>
            </div>
        `;
    }
    
    let html = '<div class="mini-cart">';
    
    cart.slice(0, 3).forEach(item => {
        html += `
            <div class="d-flex align-items-center mb-2">
                <img src="${item.image}" alt="${item.name}" 
                     style="width: 40px; height: 40px; object-fit: cover;" class="rounded me-2">
                <div class="flex-grow-1">
                    <small class="fw-bold">${item.name}</small>
                    <br>
                    <small class="text-muted">${item.quantity} x $${item.price.toFixed(2)}</small>
                </div>
            </div>
        `;
    });
    
    if (cart.length > 3) {
        html += `<small class="text-muted">and ${cart.length - 3} more items...</small>`;
    }
    
    html += `
        <hr>
        <div class="d-flex justify-content-between mb-2">
            <strong>Total: $${total.toFixed(2)}</strong>
        </div>
        <div class="d-grid gap-2">
            <a href="/cart" class="btn btn-primary btn-sm">View Cart</a>
            <a href="/checkout" class="btn btn-success btn-sm">Checkout</a>
        </div>
    </div>
    `;
    
    return html;
}

// Add to cart with quantity
function addToCartWithQuantity(id, name, price, image, quantity = 1) {
    for (let i = 0; i < quantity; i++) {
        addToCart(id, name, price, image);
    }
}

// Check if product is in cart
function isProductInCart(productId) {
    const cart = getCart();
    return cart.some(item => item.id === parseInt(productId));
}

// Get product quantity in cart
function getProductQuantityInCart(productId) {
    const cart = getCart();
    return cart.filter(item => item.id === parseInt(productId)).length;
}

// Cart validation
function validateCart() {
    const cart = getCart();
    const errors = [];
    
    if (cart.length === 0) {
        errors.push('Cart is empty');
    }
    
    cart.forEach((item, index) => {
        if (!item.id || !item.name || !item.price) {
            errors.push(`Invalid item at position ${index + 1}`);
        }
        
        if (item.price <= 0) {
            errors.push(`Invalid price for ${item.name}`);
        }
    });
    
    return {
        isValid: errors.length === 0,
        errors: errors
    };
}

// Export cart data (for backup or transfer)
function exportCartData() {
    const cart = getCart();
    const cartData = {
        items: cart,
        total: getCartTotal(),
        count: getCartItemCount(),
        exportDate: new Date().toISOString()
    };
    
    return JSON.stringify(cartData, null, 2);
}

// Import cart data (from backup or transfer)
function importCartData(cartDataString) {
    try {
        const cartData = JSON.parse(cartDataString);
        if (cartData.items && Array.isArray(cartData.items)) {
            saveCart(cartData.items);
            showCartSuccessMessage('Cart data imported successfully!');
            return true;
        }
    } catch (error) {
        console.error('Failed to import cart data:', error);
        showCartSuccessMessage('Failed to import cart data');
        return false;
    }
}

// Cart persistence across browser sessions
function initializeCartPersistence() {
    // Check if cart exists in localStorage
    const existingCart = getCart();
    
    // Clean up old items (older than 7 days)
    const sevenDaysAgo = Date.now() - (7 * 24 * 60 * 60 * 1000);
    const cleanedCart = existingCart.filter(item => {
        return item.timestamp && item.timestamp > sevenDaysAgo;
    });
    
    if (cleanedCart.length !== existingCart.length) {
        saveCart(cleanedCart);
    }
}

// Initialize cart persistence on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeCartPersistence();
});

// Handle page visibility changes to sync cart
document.addEventListener('visibilitychange', function() {
    if (!document.hidden) {
        // Page became visible, update cart count
        updateCartCount();
    }
});
