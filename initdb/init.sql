-- Create the category table
CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Create the product table
CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_level INT NOT NULL,
    imageurl TEXT,
    inventory INT NOT NULL,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

-- Insert example data into the category table
INSERT INTO category (name) VALUES
('Electronics'),
('Books'),
('Clothing'),
('Home & Kitchen');

-- Insert example data into the product table
INSERT INTO product (name, description, price, stock_level, imageurl, inventory, category_id) VALUES
('Laptop', 'High performance laptop', 1200.99, 50, 'http://example.com/laptop.jpg', 50, 1),
('Smartphone', 'Latest model smartphone', 999.99, 30, 'http://example.com/smartphone.jpg', 30, 1),
('Headphones', 'Noise cancelling headphones', 199.99, 100, 'http://example.com/headphones.jpg', 100, 1),
('Science Fiction Novel', 'A thrilling sci-fi adventure', 19.99, 200, 'http://example.com/scifi_novel.jpg', 200, 2),
('Cookbook', 'Delicious recipes for home cooking', 29.99, 150, 'http://example.com/cookbook.jpg', 150, 2),
('Jeans', 'Comfortable blue jeans', 49.99, 75, 'http://example.com/jeans.jpg', 75, 3),
('T-shirt', 'Cotton t-shirt', 15.99, 200, 'http://example.com/tshirt.jpg', 200, 3),
('Blender', 'High-speed kitchen blender', 89.99, 60, 'http://example.com/blender.jpg', 60, 4),
('Coffee Maker', 'Automatic coffee maker', 79.99, 80, 'http://example.com/coffeemaker.jpg', 80, 4),
('Vacuum Cleaner', 'Powerful vacuum cleaner', 149.99, 40, 'http://example.com/vacuumcleaner.jpg', 40, 4);
