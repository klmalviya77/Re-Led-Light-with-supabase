from flask import render_template, request, jsonify, redirect, url_for, session, flash, abort
from app import app, db
from models import Product, Category, Order, OrderItem, Catalogue
from database_service import db_service
import json
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Admin password - in production, use proper authentication
ADMIN_PASSWORD = "admin123"

@app.route('/')
def index():
    """Home page with featured products and categories"""
    try:
        # Get data from Supabase instead of local database
        categories = db_service.get_all_categories()
        featured_products = db_service.get_featured_products(6)
        featured_catalogues = db_service.get_featured_catalogues(3)

        # Initialize sample data if empty (first time setup)
        if not categories:
            db_service.initialize_sample_data()
            categories = db_service.get_all_categories()
            featured_products = db_service.get_featured_products(6)
            featured_catalogues = db_service.get_featured_catalogues(3)

        return render_template('index.html', 
                             categories=categories, 
                             featured_products=featured_products, 
                             featured_catalogues=featured_catalogues)
    except Exception as e:
        logging.error(f"Error loading homepage: {e}")
        # Fallback to local database if Supabase fails
        categories = Category.query.all()
        featured_products = Product.query.filter_by(featured=True).limit(6).all()
        featured_catalogues = Catalogue.query.filter_by(featured=True).limit(3).all()
        return render_template('index.html', categories=categories, featured_products=featured_products, featured_catalogues=featured_catalogues)

@app.route('/shop')
def shop():
    """Shop page with all products, filtering, and search"""
    category_id = request.args.get('category', type=int)
    search_query = request.args.get('search', '')

    try:
        # Use Supabase for product filtering
        if search_query:
            products = db_service.search_products(search_query)
        elif category_id:
            products = db_service.get_products_by_category(category_id)
        else:
            products = db_service.get_all_products()

        categories = db_service.get_all_categories()
        selected_category = None
        if category_id:
            for cat in categories:
                if cat['id'] == category_id:
                    selected_category = cat
                    break

        return render_template('shop.html', products=products, categories=categories, 
                             selected_category=selected_category, search_query=search_query)
    except Exception as e:
        logging.error(f"Error in shop page: {e}")
        # Fallback to local database
        query = Product.query

        if category_id:
            query = query.filter_by(category_id=category_id)

        if search_query:
            query = query.filter(Product.name.ilike(f'%{search_query}%') | 
                               Product.description.ilike(f'%{search_query}%'))

        products = query.all()
        categories = Category.query.all()
        selected_category = Category.query.get(category_id) if category_id else None

        return render_template('shop.html', products=products, categories=categories, 
                             selected_category=selected_category, search_query=search_query)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Individual product detail page"""
    try:
        # Use Supabase first
        product = db_service.get_product_by_id(product_id)
        if not product:
            abort(404)

        related_products = db_service.get_products_by_category(product['category_id'])
        # Filter out current product and limit to 4
        related_products = [p for p in related_products if p['id'] != product_id][:4]

        return render_template('product.html', product=product, related_products=related_products)
    except Exception as e:
        logging.error(f"Error loading product {product_id}: {e}")
        # Fallback to local database
        product = Product.query.get_or_404(product_id)
        related_products = Product.query.filter(
            Product.category_id == product.category_id,
            Product.id != product_id
        ).limit(4).all()

        return render_template('product.html', product=product, related_products=related_products)

@app.route('/cart')
def cart():
    """Shopping cart page"""
    return render_template('cart.html')

@app.route('/catalogues')
def catalogues():
    """Catalogues page"""
    try:
        # Use Supabase first
        catalogues = db_service.get_all_catalogues()
        featured_catalogues = db_service.get_featured_catalogues()
        return render_template('catalogues.html', catalogues=catalogues, featured_catalogues=featured_catalogues)
    except Exception as e:
        logging.error(f"Error loading catalogues: {e}")
        # Fallback to local database
        catalogues = Catalogue.query.all()
        featured_catalogues = Catalogue.query.filter_by(featured=True).all()
        return render_template('catalogues.html', catalogues=catalogues, featured_catalogues=featured_catalogues)

@app.route('/view-pdf/<int:catalogue_id>')
def view_pdf(catalogue_id):
    """View PDF catalogue"""
    try:
        # Use Supabase first
        catalogues = db_service.get_all_catalogues()
        catalogue = None
        for cat in catalogues:
            if cat['id'] == catalogue_id:
                catalogue = cat
                break

        if not catalogue:
            abort(404)

        return render_template('pdf_viewer.html', catalogue=catalogue)
    except Exception as e:
        logging.error(f"Error loading catalogue {catalogue_id}: {e}")
        # Fallback to local database
        catalogue = Catalogue.query.get_or_404(catalogue_id)
        return render_template('pdf_viewer.html', catalogue=catalogue)

@app.route('/checkout')
def checkout():
    """Checkout page"""
    return render_template('checkout.html')

@app.route('/api/submit-order', methods=['POST'])
def submit_order():
    """Submit order via AJAX"""
    try:
        data = request.json

        # Format order data for Supabase
        order_data = {
            'customer_name': data['name'],
            'customer_phone': data['phone'],
            'customer_address': data['address'],
            'total_amount': data['total'],
            'items': [{
                'product_id': item['id'],
                'quantity': item['quantity'],
                'price': item['price']
            } for item in data['items']]
        }

        # Create order using Supabase
        order = db_service.create_order(order_data)

        return jsonify({'success': True, 'order_id': order['id']})

    except Exception as e:
        logging.error(f"Error submitting order: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/contact')
def contact():
    """Contact Us page"""
    return render_template('contact.html')

@app.route('/api/submit-message', methods=['POST'])
def submit_message():
    """Submit contact message via AJAX"""
    try:
        data = request.json

        # Format message data for Supabase
        message_data = {
            'sender_name': data['name'],
            'sender_email': data['email'],
            'sender_phone': data.get('phone', ''),
            'subject': data['subject'],
            'message': data['message']
        }

        # Create message using Supabase
        message = db_service.create_message(message_data)

        return jsonify({'success': True, 'message_id': message['id']})

    except Exception as e:
        logging.error(f"Error submitting message: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/orders')
def orders():
    """Orders tracking page for users"""
    return render_template('orders.html')

@app.route('/api/user_orders')
def user_orders():
    """Get user orders by phone number using Supabase"""
    phone = request.args.get('phone')
    order_id = request.args.get('order_id')

    if not phone:
        return jsonify({'orders': []})

    try:
        orders = db_service.get_orders_by_phone(phone, order_id)

        return jsonify({
            'orders': [{
                'id': order['id'],
                'customer_name': order['customer_name'],
                'customer_phone': order['customer_phone'],
                'customer_address': order['customer_address'],
                'total_amount': order['total_amount'],
                'status': order['status'],
                'created_at': order['created_at'],
                'items': [{
                    'product_name': item['products']['name'],
                    'quantity': item['quantity'],
                    'price': item['price']
                } for item in order['order_items']]
            } for order in orders]
        })
    except Exception as e:
        logging.error(f"Error fetching orders: {e}")
        return jsonify({'orders': [], 'error': str(e)})

@app.route('/admin/catalogues', methods=['GET'])
def get_admin_catalogues():
    """Get all catalogues for admin"""
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Not authorized'}), 401

    try:
        # Use Supabase first
        catalogues = db_service.get_all_catalogues()
        return jsonify(catalogues)
    except Exception as e:
        logging.error(f"Error fetching catalogues for admin: {e}")
        # Fallback to local database
        catalogues = Catalogue.query.all()
        return jsonify([{
            'id': c.id,
            'title': c.title,
            'description': c.description,
            'pdf_url': c.pdf_url,
            'thumbnail_url': c.thumbnail_url,
            'category': c.category,
            'featured': c.featured,
            'created_at': c.created_at.isoformat()
        } for c in catalogues])

@app.route('/admin-login')
def admin_login():
    """Admin login page"""
    return render_template('admin_login.html')

@app.route('/admin-auth', methods=['POST'])
def admin_auth():
    """Enhanced admin authentication with Supabase"""
    username = request.form.get('username', 'admin')
    password = request.form.get('password')

    try:
        # First try Supabase authentication
        if db_service.verify_admin_credentials(username, password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            return redirect(url_for('admin'))
        # Fallback to hardcoded password for compatibility
        elif password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            session['admin_username'] = 'admin'
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('admin_login'))
    except Exception as e:
        logging.error(f"Admin authentication error: {e}")
        # Fallback authentication
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            session['admin_username'] = 'admin'
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('admin_login'))

@app.route('/admin')
def admin():
    """Admin dashboard"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    try:
        # Use Supabase first
        products = db_service.get_all_products()
        orders = db_service.get_all_orders()
        categories = db_service.get_all_categories()
        catalogues = db_service.get_all_catalogues()
        messages = db_service.get_all_messages()
        unread_count = db_service.get_unread_message_count()

        return render_template('admin.html', products=products, orders=orders, categories=categories, catalogues=catalogues, messages=messages, unread_count=unread_count)
    except Exception as e:
        logging.error(f"Error loading admin dashboard: {e}")
        # Fallback to local database
        products = Product.query.all()
        orders = Order.query.order_by(Order.created_at.desc()).all()
        categories = Category.query.all()
        catalogues = Catalogue.query.all()
        messages = db_service.get_all_messages()
        unread_count = db_service.get_unread_message_count()

        return render_template('admin.html', products=products, orders=orders, categories=categories, catalogues=catalogues, messages=messages, unread_count=unread_count)

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/api/admin/product', methods=['POST'])
def add_product():
    """Add new product via AJAX"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'error': 'Unauthorized'})

    try:
        data = request.json

        # Prepare product data for Supabase
        product_data = {
            'name': data['name'],
            'description': data['description'],
            'price': float(data['price']),
            'stock': int(data['stock']),
            'image_url': data['image_url'],
            'category_id': int(data['category_id']),
            'featured': data.get('featured', False)
        }

        if data.get('specifications'):
            product_data['specifications'] = data['specifications']

        # Create product in Supabase
        product = db_service.create_product(product_data)

        # Also create in local database as backup
        try:
            local_product = Product(
                name=data['name'],
                description=data['description'],
                price=float(data['price']),
                stock=int(data['stock']),
                image_url=data['image_url'],
                category_id=int(data['category_id']),
                featured=data.get('featured', False)
            )

            if data.get('specifications'):
                local_product.set_specifications(data['specifications'])

            db.session.add(local_product)
            db.session.commit()
        except Exception as local_e:
            logging.error(f"Failed to save to local database: {local_e}")

        return jsonify({'success': True, 'product_id': product['id']})

    except Exception as e:
        logging.error(f"Error adding product: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/admin/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update product via AJAX"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'error': 'Unauthorized'})

    try:
        data = request.json

        # Prepare product data for Supabase
        product_data = {
            'name': data['name'],
            'description': data['description'],
            'price': float(data['price']),
            'stock': int(data['stock']),
            'image_url': data['image_url'],
            'category_id': int(data['category_id']),
            'featured': data.get('featured', False)
        }

        if data.get('specifications'):
            product_data['specifications'] = data['specifications']

        # Update product in Supabase
        updated_product = db_service.update_product(product_id, product_data)

        # Also update in local database as backup
        try:
            product = Product.query.get(product_id)
            if product:
                product.name = data['name']
                product.description = data['description']
                product.price = float(data['price'])
                product.stock = int(data['stock'])
                product.image_url = data['image_url']
                product.category_id = int(data['category_id'])
                product.featured = data.get('featured', False)

                if data.get('specifications'):
                    product.set_specifications(data['specifications'])

                db.session.commit()
        except Exception as local_e:
            logging.error(f"Failed to update local database: {local_e}")

        return jsonify({'success': True})

    except Exception as e:
        logging.error(f"Error updating product: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/admin/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete product via AJAX"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'error': 'Unauthorized'})

    try:
        # Delete from Supabase
        db_service.delete_product(product_id)

        # Also delete from local database as backup
        try:
            product = Product.query.get(product_id)
            if product:
                db.session.delete(product)
                db.session.commit()
        except Exception as local_e:
            logging.error(f"Failed to delete from local database: {local_e}")

        return jsonify({'success': True})

    except Exception as e:
        logging.error(f"Error deleting product: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/admin/order/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status via AJAX"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'error': 'Unauthorized'})

    try:
        data = request.json

        # Update order status in Supabase
        success = db_service.update_order_status(order_id, data['status'])

        if success:
            # Also update in local database as backup
            try:
                order = Order.query.get(order_id)
                if order:
                    order.status = data['status']
                    db.session.commit()
            except Exception as local_e:
                logging.error(f"Failed to update local database: {local_e}")

            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Failed to update order status'})

    except Exception as e:
        logging.error(f"Error updating order status: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/product/<int:product_id>')
def get_product_api(product_id):
    """Get product details via API"""
    try:
        # Use Supabase first
        product = db_service.get_product_by_id(product_id)
        if not product:
            abort(404)

        return jsonify({
            'id': product['id'],
            'name': product['name'],
            'description': product['description'],
            'price': product['price'],
            'stock': product['stock'],
            'image_url': product['image_url'],
            'specifications': product.get('specifications', {})
        })
    except Exception as e:
        logging.error(f"Error getting product {product_id}: {e}")
        # Fallback to local database
        product = Product.query.get_or_404(product_id)
        return jsonify({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock,
            'image_url': product.image_url,
            'specifications': product.get_specifications()
        })

# Catalogue Management Routes
@app.route('/api/admin/catalogue', methods=['POST'])
def add_catalogue():
    """Add new catalogue via AJAX"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'error': 'Unauthorized'})

    try:
        data = request.json

        # Prepare catalogue data for Supabase
        catalogue_data = {
            'title': data['title'],
            'description': data['description'],
            'pdf_url': data['pdf_url'],
            'thumbnail_url': data.get('thumbnail_url', ''),
            'category': data.get('category', ''),
            'featured': data.get('featured', False)
        }

        # Create catalogue in Supabase
        catalogue = db_service.create_catalogue(catalogue_data)

        # Also create in local database as backup
        try:
            local_catalogue = Catalogue(
                title=data['title'],
                description=data['description'],
                pdf_url=data['pdf_url'],
                thumbnail_url=data.get('thumbnail_url', ''),
                category=data.get('category', ''),
                featured=data.get('featured', False)
            )

            db.session.add(local_catalogue)
            db.session.commit()
        except Exception as local_e:
            logging.error(f"Failed to save catalogue to local database: {local_e}")

        return jsonify({'success': True, 'catalogue_id': catalogue['id']})

    except Exception as e:
        logging.error(f"Error adding catalogue: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/admin/catalogue/<int:catalogue_id>', methods=['PUT'])
def update_catalogue(catalogue_id):
    """Update catalogue via AJAX"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'error': 'Unauthorized'})

    try:
        data = request.json

        # Prepare catalogue data for Supabase
        catalogue_data = {
            'title': data['title'],
            'description': data['description'],
            'pdf_url': data['pdf_url'],
            'thumbnail_url': data.get('thumbnail_url', ''),
            'category': data.get('category', ''),
            'featured': data.get('featured', False)
        }

        # Update catalogue in Supabase
        updated_catalogue = db_service.update_catalogue(catalogue_id, catalogue_data)

        # Also update in local database as backup
        try:
            catalogue = Catalogue.query.get(catalogue_id)
            if catalogue:
                catalogue.title = data['title']
                catalogue.description = data['description']
                catalogue.pdf_url = data['pdf_url']
                catalogue.thumbnail_url = data.get('thumbnail_url', '')
                catalogue.category = data.get('category', '')
                catalogue.featured = data.get('featured', False)
                db.session.commit()
        except Exception as local_e:
            logging.error(f"Failed to update catalogue in local database: {local_e}")

        return jsonify({'success': True})

    except Exception as e:
        logging.error(f"Error updating catalogue: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/admin/catalogue/<int:catalogue_id>', methods=['DELETE'])
def delete_catalogue(catalogue_id):
    """Delete catalogue via AJAX"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'error': 'Unauthorized'})

    try:
        # Delete from Supabase
        db_service.delete_catalogue(catalogue_id)

        # Also delete from local database as backup
        try:
            catalogue = Catalogue.query.get(catalogue_id)
            if catalogue:
                db.session.delete(catalogue)
                db.session.commit()
        except Exception as local_e:
            logging.error(f"Failed to delete catalogue from local database: {local_e}")

        return jsonify({'success': True})

    except Exception as e:
        logging.error(f"Error deleting catalogue: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/orders/<int:order_id>')
def view_order(order_id):
    """View individual order details"""
    try:
        # Use Supabase first
        order = db_service.get_order_by_id(order_id)
        if not order:
            abort(404)

        return jsonify({
            'id': order['id'],
            'customer_name': order['customer_name'],
            'customer_address': order['customer_address'],
            'total_amount': order['total_amount'],
            'status': order['status'],
            'created_at': order['created_at'],
            'items': [{
                'product_name': item['products']['name'],
                'quantity': item['quantity'],
                'price': item['price']
            } for item in order['order_items']]
        })
    except Exception as e:
        logging.error(f"Error getting order {order_id}: {e}")
        # Fallback to local database
        order = Order.query.get_or_404(order_id)
        return jsonify({
            'id': order.id,
            'customer_name': order.customer_name,
            'customer_address': order.customer_address,
            'total_amount': order.total_amount,
            'status': order.status,
            'created_at': order.created_at.isoformat(),
            'items': [{
                'product_name': item.product.name,
                'quantity': item.quantity,
                'price': item.price
            } for item in order.items]
        })

# Message Management Routes
@app.route('/api/admin/messages')
def get_admin_messages():
    """Get all messages for admin"""
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Not authorized'}), 401

    try:
        messages = db_service.get_all_messages()
        return jsonify({'messages': messages})
    except Exception as e:
        logging.error(f"Error fetching messages for admin: {e}")
        return jsonify({'messages': [], 'error': str(e)})

@app.route('/api/admin/message/<int:message_id>', methods=['GET'])
def get_message_details(message_id):
    """Get specific message details"""
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Not authorized'}), 401

    try:
        message = db_service.get_message_by_id(message_id)
        if not message:
            return jsonify({'error': 'Message not found'}), 404

        # Mark as read when viewed
        db_service.update_message_status(message_id, 'read')

        return jsonify({'message': message})
    except Exception as e:
        logging.error(f"Error fetching message {message_id}: {e}")
        return jsonify({'error': str(e)})

@app.route('/api/admin/message/<int:message_id>/reply', methods=['POST'])
def reply_to_message(message_id):
    """Reply to a message"""
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'error': 'Unauthorized'})

    try:
        data = request.json
        reply_text = data.get('reply')

        if not reply_text:
            return jsonify({'success': False, 'error': 'Reply text is required'})

        admin_username = session.get('admin_username', 'admin')
        success = db_service.reply_to_message(message_id, reply_text, admin_username)

        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Failed to send reply'})

    except Exception as e:
        logging.error(f"Error replying to message {message_id}: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/admin/message/<int:message_id>/status', methods=['PUT'])
def update_message_status_route(message_id):
    """Update message status"""
    if 'admin_logged_in' not in session:
        return jsonify({'success': False, 'error': 'Unauthorized'})

    try:
        data = request.json
        status = data.get('status')

        if status not in ['read', 'unread', 'replied']:
            return jsonify({'success': False, 'error': 'Invalid status'})

        success = db_service.update_message_status(message_id, status)

        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Failed to update status'})

    except Exception as e:
        logging.error(f"Error updating message status: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/messages/by-email')
def get_user_messages():
    """Get messages by user email"""
    email = request.args.get('email')

    if not email:
        return jsonify({'messages': []})

    try:
        messages = db_service.get_messages_by_email(email)
        return jsonify({'messages': messages})
    except Exception as e:
        logging.error(f"Error fetching user messages: {e}")
        return jsonify({'messages': [], 'error': str(e)})

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500