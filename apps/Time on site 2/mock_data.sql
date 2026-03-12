-- Create items table in Retool DB
CREATE TABLE IF NOT EXISTS items (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  price NUMERIC(10,2) NOT NULL,
  in_stock BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Insert sample data
INSERT INTO items (name, category, price, in_stock, created_at) VALUES
  ('Wireless Mouse', 'Electronics', 29.99, true, '2025-01-15 10:00:00'),
  ('USB-C Hub', 'Electronics', 49.99, true, '2025-01-20 11:30:00'),
  ('Standing Desk Mat', 'Office', 39.99, true, '2025-02-01 09:00:00'),
  ('Mechanical Keyboard', 'Electronics', 89.99, false, '2025-02-10 14:00:00'),
  ('Monitor Light Bar', 'Lighting', 34.99, true, '2025-02-15 16:00:00'),
  ('Desk Organizer', 'Office', 24.99, true, '2025-03-01 08:30:00'),
  ('Webcam HD', 'Electronics', 59.99, true, '2025-03-05 12:00:00'),
  ('Noise Cancelling Headphones', 'Audio', 149.99, false, '2025-03-10 10:00:00'),
  ('Laptop Stand', 'Office', 44.99, true, '2025-03-15 15:00:00'),
  ('Smart Power Strip', 'Electronics', 32.99, true, '2025-03-20 11:00:00');
