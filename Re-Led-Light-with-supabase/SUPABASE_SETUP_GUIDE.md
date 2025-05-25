# Supabase Setup Guide for Re Led Light

## Quick Setup Instructions

1. **Go to your Supabase Dashboard**
   - Navigate to the SQL Editor in your Supabase project

2. **Copy and paste this SQL code to create all tables:**

```sql
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
```

3. **Click "Run" to execute the SQL**

4. **Your database is now set up!** The application will automatically populate with sample data when you first visit it.

## For Netlify Deployment

Add these environment variables in your Netlify dashboard:
- `SUPABASE_URL` = Your project URL
- `SUPABASE_KEY` = Your anon/public key
- `SESSION_SECRET` = A random secret key

## Security Note
Remember to change the default admin password after setup!