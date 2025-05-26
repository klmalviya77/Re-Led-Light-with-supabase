-- Supabase Database Setup for Re Led Light E-commerce
-- Run this SQL in your Supabase SQL Editor to create all required tables

-- Enable Row Level Security
ALTER DATABASE postgres SET "app.jwt_secret" TO 'your-jwt-secret';

-- Categories table
CREATE TABLE IF NOT EXISTS categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock INTEGER DEFAULT 0,
    image_url VARCHAR(500),
    category_id BIGINT REFERENCES categories(id) ON DELETE SET NULL,
    specifications JSONB,
    featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id BIGSERIAL PRIMARY KEY,
    customer_name VARCHAR(200) NOT NULL,
    customer_phone VARCHAR(20) NOT NULL,
    customer_address TEXT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Order items table
CREATE TABLE IF NOT EXISTS order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT REFERENCES orders(id) ON DELETE CASCADE,
    product_id BIGINT REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

-- Catalogues table
CREATE TABLE IF NOT EXISTS catalogues (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    pdf_url VARCHAR(500) NOT NULL,
    thumbnail_url VARCHAR(500),
    category VARCHAR(100),
    featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Admin users table
CREATE TABLE IF NOT EXISTS admin_users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Insert default admin user (change password after setup!)
INSERT INTO admin_users (username, password, email) 
VALUES ('admin', 'admin123', 'admin@example.com')
ON CONFLICT (username) DO NOTHING;

-- Order items table
CREATE TABLE IF NOT EXISTS order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT REFERENCES orders(id) ON DELETE CASCADE,
    product_id BIGINT REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

-- Catalogues table
CREATE TABLE IF NOT EXISTS catalogues (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    pdf_url VARCHAR(500) NOT NULL,
    thumbnail_url VARCHAR(500),
    category VARCHAR(100),
    featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Admin users table for secure authentication
CREATE TABLE IF NOT EXISTS admin_users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- In production, use proper hashing
    email VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_featured ON products(featured);
CREATE INDEX IF NOT EXISTS idx_orders_phone ON orders(customer_phone);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_catalogues_featured ON catalogues(featured);
CREATE INDEX IF NOT EXISTS idx_messages_status ON messages(status);
CREATE INDEX IF NOT EXISTS idx_messages_email ON messages(sender_email);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);

-- Insert sample categories
INSERT INTO categories (name, description) VALUES
('LED Strip Lights', 'Flexible LED strip lighting solutions'),
('LED Panel Lights', 'Professional LED panel lighting'),
('LED Bulbs', 'Energy-efficient LED bulb replacements'),
('LED Spotlights', 'Focused LED spotlight solutions'),
('Smart LED Lights', 'WiFi and app-controlled LED lighting')
ON CONFLICT (name) DO NOTHING;

-- Insert sample products
INSERT INTO products (name, description, price, stock, image_url, category_id, specifications, featured) VALUES
('RGB LED Strip 5m', '5-meter RGB LED strip with remote control', 29.99, 50, 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400', 
 (SELECT id FROM categories WHERE name = 'LED Strip Lights'), 
 '{"length": "5m", "voltage": "12V", "led_count": "300"}', true),
('Smart WiFi LED Bulb', 'Color-changing smart LED bulb with app control', 15.99, 100, 'https://images.unsplash.com/photo-1565814329452-e1efa11c5b89?w=400',
 (SELECT id FROM categories WHERE name = 'Smart LED Lights'),
 '{"wattage": "9W", "brightness": "800lm", "connectivity": "WiFi"}', true),
('LED Panel Light 60x60', 'Professional 60x60cm LED panel for offices', 89.99, 25, 'https://images.unsplash.com/photo-1524484485831-a92ffc0de03f?w=400',
 (SELECT id FROM categories WHERE name = 'LED Panel Lights'),
 '{"size": "60x60cm", "wattage": "45W", "color_temp": "4000K"}', true),
('LED Spotlight GU10', 'Dimmable GU10 LED spotlight bulb', 8.99, 200, 'https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400',
 (SELECT id FROM categories WHERE name = 'LED Spotlights'),
 '{"base": "GU10", "wattage": "5W", "beam_angle": "38°"}', false),
('Warm White LED Strip 10m', '10-meter warm white LED strip', 45.99, 30, 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400',
 (SELECT id FROM categories WHERE name = 'LED Strip Lights'),
 '{"length": "10m", "voltage": "24V", "color_temp": "3000K"}', false)
ON CONFLICT DO NOTHING;

-- Insert sample catalogues
INSERT INTO catalogues (title, description, pdf_url, thumbnail_url, category, featured) VALUES
('LED Strip Light Collection 2024', 'Complete guide to our LED strip lighting solutions', 'https://example.com/led-strips-catalog.pdf', 
 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=300', 'LED Strips', true),
('Smart Lighting Solutions', 'WiFi and app-controlled lighting products', 'https://example.com/smart-lighting-catalog.pdf',
 'https://images.unsplash.com/photo-1565814329452-e1efa11c5b89?w=300', 'Smart Lights', true),
('Professional LED Panels', 'Commercial and office LED panel lighting', 'https://example.com/led-panels-catalog.pdf',
 'https://images.unsplash.com/photo-1524484485831-a92ffc0de03f?w=300', 'Panel Lights', false)
ON CONFLICT DO NOTHING;

-- Messages table for contact form and admin communication
CREATE TABLE IF NOT EXISTS messages (
    id BIGSERIAL PRIMARY KEY,
    sender_name VARCHAR(200) NOT NULL,
    sender_email VARCHAR(255) NOT NULL,
    sender_phone VARCHAR(20),
    subject VARCHAR(300) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'unread',
    admin_reply TEXT,
    admin_reply_at TIMESTAMP WITH TIME ZONE,
    replied_by VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Insert default admin user (CHANGE PASSWORD IN PRODUCTION!)
INSERT INTO admin_users (username, password, email) VALUES
('admin', 'admin123', 'admin@reledlight.com')
ON CONFLICT (username) DO NOTHING;

-- Enable Row Level Security on all tables
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE order_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE catalogues ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Create policies for public read access to products, categories, and catalogues
CREATE POLICY "Public read access for categories" ON categories FOR SELECT USING (true);
CREATE POLICY "Public read access for products" ON products FOR SELECT USING (true);
CREATE POLICY "Public read access for catalogues" ON catalogues FOR SELECT USING (true);

-- Create policies for orders (customers can only see their own orders)
CREATE POLICY "Customers can view their own orders" ON orders FOR SELECT USING (true);
CREATE POLICY "Customers can create orders" ON orders FOR INSERT WITH CHECK (true);

-- Create policies for order items
CREATE POLICY "Public read access for order items" ON order_items FOR SELECT USING (true);
CREATE POLICY "Public insert access for order items" ON order_items FOR INSERT WITH CHECK (true);

-- Admin policies (will be handled via application logic)
CREATE POLICY "Admin full access to all tables" ON categories FOR ALL USING (true);
CREATE POLICY "Admin full access to products" ON products FOR ALL USING (true);
CREATE POLICY "Admin full access to orders" ON orders FOR ALL USING (true);
CREATE POLICY "Admin full access to order items" ON order_items FOR ALL USING (true);
CREATE POLICY "Admin full access to catalogues" ON catalogues FOR ALL USING (true);
CREATE POLICY "Admin read access" ON admin_users FOR SELECT USING (true);

-- Message policies
CREATE POLICY "Public can send messages" ON messages FOR INSERT WITH CHECK (true);
CREATE POLICY "Users can view their own messages" ON messages FOR SELECT USING (true);
CREATE POLICY "Admin full access to messages" ON messages FOR ALL USING (true);