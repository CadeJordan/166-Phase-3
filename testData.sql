-- Test data converted from data/mock_data.py
-- Load with: cs166_psql cjord019_phase3_DB < testData.sql
-- Inserts are ordered to satisfy foreign keys (users -> item -> auction -> bid -> payment -> shipment).

-- Clear existing rows (child tables first)
DELETE FROM shipment;
DELETE FROM payment;
DELETE FROM bid;
DELETE FROM auction;
DELETE FROM item;
DELETE FROM users;

-- Users
INSERT INTO users (login, password, phone_num, address, role, favorite_category) VALUES
('buyer1',  'buyer123',  '555-0101', '123 Main St, Austin, TX 78701',      'Buyer',  'Electronics'),
('buyer2',  'buyer456',  '555-0102', '456 Oak Ave, Dallas, TX 75201',      'Buyer',  'Collectibles'),
('seller1', 'seller123', '555-0201', '789 Pine Rd, Houston, TX 77001',     'Seller', 'Electronics'),
('seller2', 'seller456', '555-0202', '321 Elm Blvd, San Antonio, TX 78201','Seller', 'Fashion'),
('admin1',  'admin123',  '555-0301', '100 Admin Way, Austin, TX 78702',    'Admin',  NULL);

-- Items
INSERT INTO item (item_id, item_name, category, starting_price, image_url, item_condition, description, seller_login, seller_role) VALUES
(1, 'Vintage Canon AE-1 Camera',                'Electronics',   75.00,  'https://placehold.co/400x400/e8e8e8/666?text=Camera',     'Used - Good',     'Classic 35mm film camera in working condition. Includes original lens cap.', 'seller1', 'Seller'),
(2, 'Nintendo Switch OLED Console',             'Electronics',   200.00, 'https://placehold.co/400x400/e8e8e8/666?text=Switch',     'Used - Like New', 'White OLED model with dock and two Joy-Con controllers.',                    'seller1', 'Seller'),
(3, '1952 Mickey Mantle Rookie Card (Reprint)', 'Collectibles',  25.00,  'https://placehold.co/400x400/e8e8e8/666?text=Card',       'New',             'High-quality reprint in protective sleeve.',                                 'seller2', 'Seller'),
(4, 'Levi''s 501 Original Jeans',               'Fashion',       30.00,  'https://placehold.co/400x400/e8e8e8/666?text=Jeans',      'Used - Good',     'Size 32x32, dark wash, minimal wear.',                                       'seller2', 'Seller'),
(5, 'Weber Spirit II E-310 Grill',              'Home & Garden', 150.00, 'https://placehold.co/400x400/e8e8e8/666?text=Grill',      'Used - Good',     '3-burner gas grill with cover. Pickup only.',                                'seller1', 'Seller'),
(6, 'Wilson Pro Staff Tennis Racket',           'Sports',        45.00,  'https://placehold.co/400x400/e8e8e8/666?text=Racket',     'Used - Like New', 'Grip size 4 3/8, freshly restrung.',                                         'seller2', 'Seller'),
(7, 'LEGO Star Wars Millennium Falcon',         'Toys',          80.00,  'https://placehold.co/400x400/e8e8e8/666?text=LEGO',       'Used - Good',     'Complete set with box and instructions.',                                    'seller1', 'Seller'),
(8, 'Sony WH-1000XM4 Headphones',               'Electronics',   120.00, 'https://placehold.co/400x400/e8e8e8/666?text=Headphones', 'Used - Like New', 'Black, noise-cancelling, includes carrying case.',                           'seller1', 'Seller');

-- Auctions
INSERT INTO auction (auction_id, item_id, seller_login, seller_role, current_highest_bid, auction_status, winner_login, winner_role) VALUES
(1, 1, 'seller1', 'Seller', 95.00,  'Active', NULL,     NULL),
(2, 2, 'seller1', 'Seller', 245.00, 'Active', NULL,     NULL),
(3, 3, 'seller2', 'Seller', 38.50,  'Active', NULL,     NULL),
(4, 4, 'seller2', 'Seller', 42.00,  'Active', NULL,     NULL),
(5, 5, 'seller1', 'Seller', 175.00, 'Active', NULL,     NULL),
(6, 6, 'seller2', 'Seller', 55.00,  'Closed', 'buyer1', 'Buyer'),
(7, 7, 'seller1', 'Seller', 110.00, 'Closed', 'buyer2', 'Buyer'),
(8, 8, 'seller1', 'Seller', 145.00, 'Active', NULL,     NULL);

-- Bids
INSERT INTO bid (bid_id, auction_id, buyer_login, buyer_role, bid_amount, bid_timestamp) VALUES
(1,  1, 'buyer1', 'Buyer', 80.00,  '2026-05-28 10:15:00'),
(2,  1, 'buyer2', 'Buyer', 85.00,  '2026-05-28 14:30:00'),
(3,  1, 'buyer1', 'Buyer', 95.00,  '2026-05-29 09:00:00'),
(4,  2, 'buyer1', 'Buyer', 210.00, '2026-05-27 11:00:00'),
(5,  2, 'buyer2', 'Buyer', 225.00, '2026-05-28 16:45:00'),
(6,  2, 'buyer1', 'Buyer', 245.00, '2026-05-30 08:20:00'),
(7,  3, 'buyer2', 'Buyer', 30.00,  '2026-05-29 12:00:00'),
(8,  3, 'buyer1', 'Buyer', 35.00,  '2026-05-30 10:30:00'),
(9,  3, 'buyer2', 'Buyer', 38.50,  '2026-06-01 15:00:00'),
(10, 4, 'buyer1', 'Buyer', 35.00,  '2026-05-30 09:15:00'),
(11, 4, 'buyer2', 'Buyer', 42.00,  '2026-06-02 11:00:00'),
(12, 5, 'buyer2', 'Buyer', 160.00, '2026-06-01 13:00:00'),
(13, 5, 'buyer1', 'Buyer', 175.00, '2026-06-03 10:00:00'),
(14, 6, 'buyer1', 'Buyer', 50.00,  '2026-05-20 10:00:00'),
(15, 6, 'buyer2', 'Buyer', 55.00,  '2026-05-22 14:00:00'),
(16, 7, 'buyer2', 'Buyer', 100.00, '2026-05-18 09:00:00'),
(17, 7, 'buyer1', 'Buyer', 105.00, '2026-05-19 11:00:00'),
(18, 7, 'buyer2', 'Buyer', 110.00, '2026-05-21 16:00:00'),
(19, 8, 'buyer1', 'Buyer', 130.00, '2026-06-02 08:00:00'),
(20, 8, 'buyer2', 'Buyer', 145.00, '2026-06-04 12:30:00');

-- Payments
INSERT INTO payment (payment_id, auction_id, buyer_login, buyer_role, amount, payment_status) VALUES
(1, 6, 'buyer1', 'Buyer', 55.00,  'Completed'),
(2, 7, 'buyer2', 'Buyer', 110.00, 'Pending');

-- Shipments
INSERT INTO shipment (shipment_id, auction_id, address, shipment_status, tracking_number) VALUES
(1, 6, '123 Main St, Austin, TX 78701', 'Delivered', '1Z999AA10123456784'),
(2, 7, '456 Oak Ave, Dallas, TX 75201', 'Pending',   NULL);
