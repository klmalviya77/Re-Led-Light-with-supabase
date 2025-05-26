// Admin panel functionality for Re Led Light website

// Global variables
let products = [];
let orders = [];

// Initialize admin functionality
document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
    loadOrders();
    loadCatalogues();
});

// Load products data
function loadProducts() {
    // Products are already rendered by the template
    // This function can be used for dynamic loading in the future
}

// Load orders data
function loadOrders() {
    // Orders are already rendered by the template
    // This function can be used for dynamic loading in the future
}

// Add/Edit Product Functions
function editProduct(productId) {
    // Find product data from the table
    const row = document.querySelector(`button[onclick="editProduct(${productId})"]`).closest('tr');
    const cells = row.querySelectorAll('td');

    // Populate form
    document.getElementById('productId').value = productId;
    document.getElementById('productName').value = cells[1].textContent.trim();
    document.getElementById('productPrice').value = parseFloat(cells[3].textContent.replace('$', ''));
    document.getElementById('productStock').value = parseInt(cells[4].textContent.trim());
    document.getElementById('productImage').value = cells[0].querySelector('img').src;

    // Set category (need to find by name)
    const categoryName = cells[2].textContent.trim();
    const categorySelect = document.getElementById('productCategory');
    for (let option of categorySelect.options) {
        if (option.text === categoryName) {
            option.selected = true;
            break;
        }
    }

    // Set featured status
    const featuredBadge = cells[5].querySelector('.badge');
    document.getElementById('productFeatured').checked = featuredBadge.textContent.includes('Featured');

    // Change modal title
    document.getElementById('productModalTitle').textContent = 'Edit Product';

    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('productModal'));
    modal.show();
}

function saveProduct() {
    const productId = document.getElementById('productId').value;
    const isEdit = productId !== '';

    const productData = {
        name: document.getElementById('productName').value,
        description: document.getElementById('productDescription').value,
        price: parseFloat(document.getElementById('productPrice').value),
        stock: parseInt(document.getElementById('productStock').value),
        image_url: document.getElementById('productImage').value,
        category_id: parseInt(document.getElementById('productCategory').value),
        featured: document.getElementById('productFeatured').checked,
        specifications: {} // Can be extended to include specifications
    };

    const url = isEdit ? `/api/admin/product/${productId}` : '/api/admin/product';
    const method = isEdit ? 'PUT' : 'POST';

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(productData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccessMessage(isEdit ? 'Product updated successfully!' : 'Product added successfully!');

            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('productModal'));
            modal.hide();

            // Reset form
            document.getElementById('productForm').reset();
            document.getElementById('productId').value = '';
            document.getElementById('productModalTitle').textContent = 'Add Product';

            // Reload page to show changes
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showErrorMessage(data.error || 'Failed to save product');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showErrorMessage('Network error occurred');
    });
}

function deleteProduct(productId) {
    if (!confirm('Are you sure you want to delete this product? This action cannot be undone.')) {
        return;
    }

    fetch(`/api/admin/product/${productId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccessMessage('Product deleted successfully!');

            // Remove row from table
            const button = document.querySelector(`button[onclick="deleteProduct(${productId})"]`);
            const row = button.closest('tr');
            row.remove();
        } else {
            showErrorMessage(data.error || 'Failed to delete product');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showErrorMessage('Network error occurred');
    });
}

// Order Management Functions
function updateOrderStatus(orderId, newStatus) {
    fetch(`/api/admin/order/${orderId}/status`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccessMessage('Order status updated successfully!');
        } else {
            showErrorMessage(data.error || 'Failed to update order status');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showErrorMessage('Network error occurred');
    });
}

function viewOrderDetails(orderId) {
    // This would typically fetch order details from the server
    // For now, we'll show a placeholder modal
    const orderDetailsHtml = `
        <div class="text-center py-4">
            <i class="fas fa-info-circle fa-3x text-info mb-3"></i>
            <h5>Order #${orderId}</h5>
            <p>Order details feature coming soon...</p>
            <p class="text-muted">This will show detailed order information including items, customer details, and shipping information.</p>
        </div>
    `;

    document.getElementById('orderDetails').innerHTML = orderDetailsHtml;
    const modal = new bootstrap.Modal(document.getElementById('orderModal'));
    modal.show();
}

// Utility Functions
function showSuccessMessage(message) {
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

    // Auto dismiss after 3 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 3000);
}

function showErrorMessage(message) {
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

    // Auto dismiss after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}

// Reset product form when modal is closed
document.getElementById('productModal').addEventListener('hidden.bs.modal', function() {
    document.getElementById('productForm').reset();
    document.getElementById('productId').value = '';
    document.getElementById('productModalTitle').textContent = 'Add Product';
});

// Form validation
function validateProductForm() {
    const name = document.getElementById('productName').value.trim();
    const description = document.getElementById('productDescription').value.trim();
    const price = parseFloat(document.getElementById('productPrice').value);
    const stock = parseInt(document.getElementById('productStock').value);
    const imageUrl = document.getElementById('productImage').value.trim();

    const errors = [];

    if (!name) errors.push('Product name is required');
    if (!description) errors.push('Product description is required');
    if (!price || price <= 0) errors.push('Valid price is required');
    if (!stock || stock < 0) errors.push('Valid stock quantity is required');
    if (!imageUrl) errors.push('Image URL is required');

    return {
        isValid: errors.length === 0,
        errors: errors
    };
}

// Enhanced save product with validation
function saveProductWithValidation() {
    const validation = validateProductForm();

    if (!validation.isValid) {
        showErrorMessage('Please fix the following errors:\n' + validation.errors.join('\n'));
        return;
    }

    saveProduct();
}

// Auto-save draft functionality
let autoSaveDraftTimer;

function autoSaveDraft() {
    clearTimeout(autoSaveDraftTimer);
    autoSaveDraftTimer = setTimeout(() => {
        const formData = {
            name: document.getElementById('productName').value,
            description: document.getElementById('productDescription').value,
            price: document.getElementById('productPrice').value,
            stock: document.getElementById('productStock').value,
            image_url: document.getElementById('productImage').value,
            category_id: document.getElementById('productCategory').value,
            featured: document.getElementById('productFeatured').checked
        };

        localStorage.setItem('productDraft', JSON.stringify(formData));
    }, 1000);
}

// Load draft on form open
function loadDraft() {
    const draft = localStorage.getItem('productDraft');
    if (draft) {
        const formData = JSON.parse(draft);
        document.getElementById('productName').value = formData.name || '';
        document.getElementById('productDescription').value = formData.description || '';
        document.getElementById('productPrice').value = formData.price || '';
        document.getElementById('productStock').value = formData.stock || '';
        document.getElementById('productImage').value = formData.image_url || '';
        document.getElementById('productCategory').value = formData.category_id || '';
        document.getElementById('productFeatured').checked = formData.featured || false;
    }
}

// Catalogue Management Functions
function loadCatalogues() {
    fetch('/admin/catalogues')
        .then(response => response.json())
        .then(catalogues => {
            const tbody = document.getElementById('catalogues-table-body');
            tbody.innerHTML = '';

            catalogues.forEach(catalogue => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${catalogue.id}</td>
                    <td>${catalogue.title}</td>
                    <td>${catalogue.category || 'N/A'}</td>
                    <td>
                        <span class="badge ${catalogue.featured ? 'bg-warning' : 'bg-secondary'}">
                            ${catalogue.featured ? 'Featured' : 'Regular'}
                        </span>
                    </td>
                    <td>${new Date(catalogue.created_at).toLocaleDateString()}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteCatalogue(${catalogue.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                        <a href="${catalogue.pdf_url}" target="_blank" class="btn btn-sm btn-outline-primary">
                            <i class="fas fa-external-link-alt"></i>
                        </a>
                    </td>
                `;
                tbody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error loading catalogues:', error);
            showErrorMessage('Failed to load catalogues');
        });
}

function saveCatalogue() {
    const formData = {
        title: document.getElementById('catalogueTitle').value,
        description: document.getElementById('catalogueDescription').value,
        pdf_url: document.getElementById('cataloguePdfUrl').value,
        thumbnail_url: document.getElementById('catalogueThumbnail').value,
        category: document.getElementById('catalogueCategory').value,
        featured: document.getElementById('catalogueFeatured').checked
    };

    if (!formData.title || !formData.pdf_url) {
        showErrorMessage('Please fill in all required fields');
        return;
    }

    fetch('/api/admin/catalogue', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccessMessage('Catalogue added successfully');
            document.getElementById('catalogueForm').reset();
            bootstrap.Modal.getInstance(document.getElementById('catalogueModal')).hide();
            loadCatalogues();
        } else {
            showErrorMessage(data.message || 'Failed to add catalogue');
        }
    })
    .catch(error => {
        console.error('Error saving catalogue:', error);
        showErrorMessage('Failed to save catalogue');
    });
}

function deleteCatalogue(catalogueId) {
    if (confirm('Are you sure you want to delete this catalogue?')) {
        fetch(`/api/admin/catalogue/${catalogueId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showSuccessMessage('Catalogue deleted successfully');
                loadCatalogues();
            } else {
                showErrorMessage(data.message || 'Failed to delete catalogue');
            }
        })
        .catch(error => {
            console.error('Error deleting catalogue:', error);
            showErrorMessage('Failed to delete catalogue');
        });
    }
}

// Clear draft
function clearDraft() {
    localStorage.removeItem('productDraft');
}

// Add event listeners for auto-save
document.addEventListener('DOMContentLoaded', function() {
    const formInputs = [
        'productName',
        'productDescription', 
        'productPrice',
        'productStock',
        'productImage',
        'productCategory',
        'productFeatured'
    ];

    formInputs.forEach(inputId => {
        const element = document.getElementById(inputId);
        if (element) {
            element.addEventListener('input', autoSaveDraft);
            element.addEventListener('change', autoSaveDraft);
        }
    });
});

// Search and filter functionality
function filterProducts(searchTerm) {
    const rows = document.querySelectorAll('#products tbody tr');

    rows.forEach(row => {
        const productName = row.cells[1].textContent.toLowerCase();
        const category = row.cells[2].textContent.toLowerCase();
        const isMatch = productName.includes(searchTerm.toLowerCase()) || 
                       category.includes(searchTerm.toLowerCase());

        row.style.display = isMatch ? '' : 'none';
    });
}

function filterOrders(status) {
    const rows = document.querySelectorAll('#orders tbody tr');

    rows.forEach(row => {
        const orderStatus = row.cells[4].querySelector('select').value;
        const isMatch = status === 'all' || orderStatus === status;

        row.style.display = isMatch ? '' : 'none';
    });
}

// Export functionality
function exportProducts() {
    // This would generate a CSV or JSON export of products
    console.log('Export products functionality would be implemented here');
    showSuccessMessage('Export feature coming soon!');
}

function exportOrders() {
    // This would generate a CSV or JSON export of orders
    console.log('Export orders functionality would be implemented here');
    showSuccessMessage('Export feature coming soon!');
}

// Bulk operations
function bulkDeleteProducts(productIds) {
    if (!confirm(`Are you sure you want to delete ${productIds.length} products? This action cannot be undone.`)) {
        return;
    }

    // Implementation for bulk delete
    console.log('Bulk delete products:', productIds);
    showSuccessMessage('Bulk delete feature coming soon!');
}

function bulkUpdateOrderStatus(orderIds, newStatus) {
    // Implementation for bulk status update
    console.log('Bulk update orders:', orderIds, newStatus);
    showSuccessMessage('Bulk update feature coming soon!');
}

editCatalogueModal.show();
}

// Message Management Functions
let currentMessageId = null;

function refreshMessages() {
    fetch('/api/admin/messages')
        .then(response => response.json())
        .then(data => {
            if (data.messages) {
                updateMessagesTable(data.messages);
            }
        })
        .catch(error => {
            console.error('Error refreshing messages:', error);
            showAlert('Error refreshing messages', 'danger');
        });
}

function updateMessagesTable(messages) {
    const tbody = document.querySelector('#messagesTable tbody');
    tbody.innerHTML = '';

    messages.forEach(message => {
        const row = document.createElement('tr');
        const statusClass = getMessageStatusClass(message.status);
        const date = new Date(message.created_at).toLocaleDateString();

        row.innerHTML = `
            <td>${message.id}</td>
            <td>
                <div>${message.sender_name}</div>
                <small class="text-muted">${message.sender_email}</small>
            </td>
            <td>${message.subject}</td>
            <td>${date}</td>
            <td>
                <span class="badge ${statusClass}">
                    ${message.status.charAt(0).toUpperCase() + message.status.slice(1)}
                </span>
            </td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="viewMessage(${message.id})">
                    <i class="bi bi-eye"></i> View
                </button>
                ${message.status !== 'replied' ? `
                <button class="btn btn-sm btn-success" onclick="replyToMessage(${message.id})">
                    <i class="bi bi-reply"></i> Reply
                </button>
                ` : ''}
            </td>
        `;

        tbody.appendChild(row);
    });
}

function getMessageStatusClass(status) {
    switch(status) {
        case 'unread': return 'bg-warning';
        case 'read': return 'bg-info';
        case 'replied': return 'bg-success';
        default: return 'bg-secondary';
    }
}

function viewMessage(messageId) {
    currentMessageId = messageId;

    fetch(`/api/admin/message/${messageId}`)
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                displayMessageDetails(data.message);
                const messageViewModal = new bootstrap.Modal(document.getElementById('messageViewModal'));
                messageViewModal.show();
            }
        })
        .catch(error => {
            console.error('Error fetching message:', error);
            showAlert('Error loading message', 'danger');
        });
}

function displayMessageDetails(message) {
    const content = document.getElementById('messageViewContent');
    const date = new Date(message.created_at).toLocaleString();
    const statusClass = getMessageStatusClass(message.status);

    let replySection = '';
    if (message.admin_reply) {
        const replyDate = new Date(message.admin_reply_at).toLocaleString();
        replySection = `
            <div class="bg-light p-3 rounded mt-3">
                <h6>Admin Reply</h6>
                <p>${message.admin_reply}</p>
                <small class="text-muted">Replied on ${replyDate} by ${message.replied_by}</small>
            </div>
        `;
    }

    content.innerHTML = `
        <div class="mb-3">
            <h6>From: ${message.sender_name}</h6>
            <p class="text-muted mb-1">Email: ${message.sender_email}</p>
            ${message.sender_phone ? `<p class="text-muted mb-1">Phone: ${message.sender_phone}</p>` : ''}
            <p class="text-muted mb-1">Date: ${date}</p>
            <span class="badge ${statusClass}">${message.status.charAt(0).toUpperCase() + message.status.slice(1)}</span>
        </div>

        <div class="mb-3">
            <h6>Subject: ${message.subject}</h6>
        </div>

        <div class="mb-3">
            <h6>Message:</h6>
            <p class="border p-3 rounded">${message.message}</p>
        </div>

        ${replySection}
    `;

    // Update reply button visibility
    const replyBtn = document.getElementById('replyFromViewBtn');
    if (message.status === 'replied') {
        replyBtn.style.display = 'none';
    } else {
        replyBtn.style.display = 'block';
    }
}

function replyToMessage(messageId) {
    currentMessageId = messageId;
    document.getElementById('replyMessageId').value = messageId;
    document.getElementById('replyText').value = '';

    const messageReplyModal = new bootstrap.Modal(document.getElementById('messageReplyModal'));
    messageReplyModal.show();
}

function showReplyForm() {
    // Close view modal and open reply modal
    const messageViewModal = bootstrap.Modal.getInstance(document.getElementById('messageViewModal'));
    messageViewModal.hide();

    setTimeout(() => {
        replyToMessage(currentMessageId);
    }, 300);
}

function sendReply() {
    const messageId = document.getElementById('replyMessageId').value;
    const replyText = document.getElementById('replyText').value.trim();

    if (!replyText) {
        showAlert('Please enter a reply message', 'warning');
        return;
    }

    fetch(`/api/admin/message/${messageId}/reply`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            reply: replyText
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Reply sent successfully', 'success');

            // Close modal
            const messageReplyModal = bootstrap.Modal.getInstance(document.getElementById('messageReplyModal'));
            messageReplyModal.hide();

            // Refresh messages
            refreshMessages();
        } else {
            showAlert('Error: ' + (data.error || 'Failed to send reply'), 'danger');
        }
    })
    .catch(error => {
        console.error('Error sending reply:', error);
        showAlert('Error sending reply', 'danger');
    });
}