"""
Database service module for Supabase integration
Maintains all existing functionality while using real Supabase data
"""
import os
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any
from supabase_config import supabase

class DatabaseService:
    """Database service for handling all Supabase operations"""

    def __init__(self):
        self.client = supabase

    # Category operations
    def get_all_categories(self) -> List[Dict]:
        """Get all categories from Supabase"""
        try:
            response = self.client.table('categories').select('*').execute()
            return response.data if response.data else []
        except Exception as e:
            logging.error(f"Error fetching categories: {e}")
            return []

    def create_category(self, name: str, description: str = None) -> Dict:
        """Create a new category"""
        try:
            data = {"name": name, "description": description}
            response = self.client.table('categories').insert(data).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logging.error(f"Error creating category: {e}")
            raise

    # Product operations
    def get_all_products(self) -> List[Dict]:
        """Get all products with category information"""
        try:
            response = self.client.table('products').select('*, categories(name)').execute()
            return response.data if response.data else []
        except Exception as e:
            logging.error(f"Error fetching products: {e}")
            return []

    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """Get a single product by ID"""
        try:
            response = self.client.table('products').select('*, categories(name)').eq('id', product_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logging.error(f"Error fetching product {product_id}: {e}")
            return None

    def get_featured_products(self, limit: int = 6) -> List[Dict]:
        """Get featured products"""
        try:
            response = self.client.table('products').select('*, categories(name)').eq('featured', True).limit(limit).execute()
            return response.data if response.data else []
        except Exception as e:
            logging.error(f"Error fetching featured products: {e}")
            return []

    def get_products_by_category(self, category_id: int) -> List[Dict]:
        """Get products by category ID"""
        try:
            response = self.client.table('products').select('*, categories(name)').eq('category_id', category_id).execute()
            return response.data if response.data else []
        except Exception as e:
            logging.error(f"Error fetching products for category {category_id}: {e}")
            return []

    def search_products(self, query: str) -> List[Dict]:
        """Search products by name or description"""
        try:
            response = self.client.table('products').select('*, categories(name)').or_(f'name.ilike.%{query}%,description.ilike.%{query}%').execute()
            return response.data if response.data else []
        except Exception as e:
            logging.error(f"Error searching products: {e}")
            return []

    def create_product(self, product_data: Dict) -> Dict:
        """Create a new product"""
        try:
            product_data['created_at'] = datetime.utcnow().isoformat()
            response = self.client.table('products').insert(product_data).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logging.error(f"Error creating product: {e}")
            raise

    def update_product(self, product_id: int, product_data: Dict) -> Dict:
        """Update a product"""
        try:
            response = self.client.table('products').update(product_data).eq('id', product_id).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logging.error(f"Error updating product {product_id}: {e}")
            raise

    def delete_product(self, product_id: int) -> bool:
        """Delete a product"""
        try:
            self.client.table('products').delete().eq('id', product_id).execute()
            return True
        except Exception as e:
            logging.error(f"Error deleting product {product_id}: {e}")
            raise

    def update_product_stock(self, product_id: int, quantity_change: int) -> bool:
        """Update product stock (decrease for orders)"""
        try:
            product = self.get_product_by_id(product_id)
            if not product:
                return False
            new_stock = max(0, product['stock'] + quantity_change)
            self.client.table('products').update({'stock': new_stock}).eq('id', product_id).execute()
            return True
        except Exception as e:
            logging.error(f"Error updating stock for product {product_id}: {e}")
            return False

    # Order operations
    def create_order(self, order_data: Dict) -> Dict:
        """Create a new order with items"""
        try:
            # Start a Supabase transaction
            order_data['created_at'] = datetime.utcnow().isoformat()
            order_data['status'] = 'pending'

            # Insert order
            order_response = self.client.table('orders').insert(order_data).execute()
            if not order_response.data:
                raise Exception("Failed to create order")

            order = order_response.data[0]

            # Insert order items
            items = order_data.pop('items', [])
            for item in items:
                item['order_id'] = order['id']
                self.client.table('order_items').insert(item).execute()

                # Update product stock
                self.update_product_stock(item['product_id'], -item['quantity'])

            return order
        except Exception as e:
            logging.error(f"Error creating order: {e}")
            raise

    def create_order_item(self, order_item_data: Dict) -> Dict:
        """Create a new order item"""
        try:
            response = self.client.table('order_items').insert(order_item_data).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logging.error(f"Error creating order item: {e}")
            raise

    def get_all_orders(self) -> List[Dict]:
        """Get all orders with items"""
        try:
            response = self.client.table('orders').select('*, order_items(*, products(name))').order('created_at', desc=True).execute()
            return response.data if response.data else []
        except Exception as e:
            logging.error(f"Error fetching orders: {e}")
            return []

    def get_orders_by_phone(self, phone: str, order_id: int = None) -> List[Dict]:
        """Get orders by customer phone number"""
        try:
            query = self.client.table('orders').select(
                '*, order_items(*, products(name))'
            ).eq('customer_phone', phone)

            if order_id:
                query = query.eq('id', order_id)

            response = query.order('created_at', desc=True).execute()
            return response.data if response.data else []
        except Exception as e:
            logging.error(f"Error fetching orders by phone: {e}")
            return []

    def get_order_by_id(self, order_id: int) -> Optional[Dict]:
        """Get order by ID with items"""
        try:
            response = self.client.table('orders').select(
                '*, order_items(*, products(name))'
            ).eq('id', order_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logging.error(f"Error fetching order {order_id}: {e}")
            return None

    def update_order_status(self, order_id: int, status: str) -> bool:
        """Update order status"""
        try:
            self.client.table('orders').update({'status': status}).eq('id', order_id).execute()
            return True
        except Exception as e:
            logging.error(f"Error updating order status: {e}")
            return False

    # Catalogue operations
    def get_all_catalogues(self) -> List[Dict]:
        """Get all catalogues"""
        try:
            response = self.client.table('catalogues').select('*').execute()
            return response.data if response.data else []
        except Exception as e:
            logging.error(f"Error fetching catalogues: {e}")
            return []

    def get_featured_catalogues(self, limit: int = 3) -> List[Dict]:
        """Get featured catalogues"""
        try:
            response = self.client.table('catalogues').select('*').eq('featured', True).limit(limit).execute()
            return response.data if response.data else []
        except Exception as e:
            logging.error(f"Error fetching featured catalogues: {e}")
            return []

    def create_catalogue(self, catalogue_data: Dict) -> Dict:
        """Create a new catalogue"""
        try:
            catalogue_data['created_at'] = datetime.utcnow().isoformat()
            response = self.client.table('catalogues').insert(catalogue_data).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logging.error(f"Error creating catalogue: {e}")
            raise

    def delete_catalogue(self, catalogue_id: int) -> bool:
        """Delete a catalogue"""
        try:
            self.client.table('catalogues').delete().eq('id', catalogue_id).execute()
            return True
        except Exception as e:
            logging.error(f"Error deleting catalogue {catalogue_id}: {e}")
            raise

    # Admin operations
    def verify_admin_credentials(self, username: str, password: str) -> bool:
        """Verify admin credentials against Supabase"""
        try:
            response = self.client.table('admin_users').select('*').eq('username', username).execute()
            if response.data:
                admin_user = response.data[0]
                # In production, you should use proper password hashing
                return admin_user.get('password') == password
            return False
        except Exception as e:
            logging.error(f"Error verifying admin credentials: {e}")
            return False

    # Initialize sample data
    def initialize_sample_data(self):
        """Initialize database with sample data if tables are empty"""
        try:
            # Check if categories exist
            categories = self.get_all_categories()
            if not categories:
                self._create_sample_categories()

            # Check if products exist
            products = self.get_all_products()
            if not products:
                self._create_sample_products()

            # Check if catalogues exist
            catalogues = self.get_all_catalogues()
            if not catalogues:
                self._create_sample_catalogues()

        except Exception as e:
            logging.error(f"Error initializing sample data: {e}")

    def _create_sample_categories(self):
        """Create sample categories"""
        sample_categories = [
            {"name": "LED Strip Lights", "description": "Flexible LED strip lighting solutions"},
            {"name": "LED Panel Lights", "description": "Professional LED panel lighting"},
            {"name": "LED Bulbs", "description": "Energy-efficient LED bulb replacements"},
            {"name": "LED Spotlights", "description": "Focused LED spotlight solutions"},
            {"name": "Smart LED Lights", "description": "WiFi and app-controlled LED lighting"}
        ]

        for category in sample_categories:
            self.create_category(category["name"], category["description"])

    def _create_sample_products(self):
        """Create sample products"""
        # Get category IDs first
        categories = self.get_all_categories()
        category_map = {cat['name']: cat['id'] for cat in categories}

        sample_products = [
            {
                "name": "RGB LED Strip 5m",
                "description": "5-meter RGB LED strip with remote control",
                "price": 29.99,
                "stock": 50,
                "image_url": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400",
                "category_id": category_map.get("LED Strip Lights"),
                "specifications": '{"length": "5m", "voltage": "12V", "led_count": "300"}',
                "featured": True
            },
            {
                "name": "Smart WiFi LED Bulb",
                "description": "Color-changing smart LED bulb with app control",
                "price": 15.99,
                "stock": 100,
                "image_url": "https://images.unsplash.com/photo-1565814329452-e1efa11c5b89?w=400",
                "category_id": category_map.get("Smart LED Lights"),
                "specifications": '{"wattage": "9W", "brightness": "800lm", "connectivity": "WiFi"}',
                "featured": True
            }
        ]

        for product in sample_products:
            if product["category_id"]:  # Only create if category exists
                self.create_product(product)

    def _create_sample_catalogues(self):
        """Create sample catalogues"""
        sample_catalogues = [
            {
                "title": "LED Strip Light Collection",
                "description": "Complete guide to our LED strip lighting solutions",
                "pdf_url": "https://example.com/led-strips-catalog.pdf",
                "thumbnail_url": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=300",
                "category": "LED Strips",
                "featured": True
            }
        ]

        for catalogue in sample_catalogues:
            self.create_catalogue(catalogue)

    # Message operations
    def create_message(self, message_data: Dict) -> Dict:
        """Create a new contact message"""
        try:
            message_data['created_at'] = datetime.utcnow().isoformat()
            message_data['status'] = 'unread'
            response = self.client.table('messages').insert(message_data).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logging.error(f"Error creating message: {e}")
            raise

    def get_all_messages(self) -> List[Dict]:
        """Get all messages for admin panel"""
        try:
            response = self.client.table('messages').select('*').order('created_at', desc=True).execute()
            return response.data if response.data else []
        except Exception as e:
            logging.error(f"Error fetching messages: {e}")
            return []

    def get_messages_by_email(self, email: str) -> List[Dict]:
        """Get messages by sender email"""
        try:
            response = self.client.table('messages').select('*').eq('sender_email', email).order('created_at', desc=True).execute()
            return response.data if response.data else []
        except Exception as e:
            logging.error(f"Error fetching messages by email: {e}")
            return []

    def get_message_by_id(self, message_id: int) -> Optional[Dict]:
        """Get message by ID"""
        try:
            response = self.client.table('messages').select('*').eq('id', message_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logging.error(f"Error fetching message {message_id}: {e}")
            return None

    def update_message_status(self, message_id: int, status: str) -> bool:
        """Update message status (read/unread)"""
        try:
            self.client.table('messages').update({'status': status}).eq('id', message_id).execute()
            return True
        except Exception as e:
            logging.error(f"Error updating message status: {e}")
            return False

    def reply_to_message(self, message_id: int, reply_text: str, admin_username: str) -> bool:
        """Add admin reply to a message"""
        try:
            reply_data = {
                'admin_reply': reply_text,
                'admin_reply_at': datetime.utcnow().isoformat(),
                'replied_by': admin_username,
                'status': 'replied'
            }
            self.client.table('messages').update(reply_data).eq('id', message_id).execute()
            return True
        except Exception as e:
            logging.error(f"Error replying to message: {e}")
            return False

    def get_unread_message_count(self) -> int:
        """Get count of unread messages"""
        try:
            response = self.client.table('messages').select('id', count='exact').eq('status', 'unread').execute()
            return response.count if response.count else 0
        except Exception as e:
            logging.error(f"Error getting unread message count: {e}")
            return 0


# Initialize the database service
db_service = DatabaseService()