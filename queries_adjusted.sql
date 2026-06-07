-- queries.sql adjusted to match your schema and avoid foreign key errors
-- This file creates its own small demo data first, then runs the feature queries.
-- It can be run after schema.sql and index.sql.

-- Required demo users
INSERT INTO users (login, password, phone_num, address, role, favorite_category) VALUES ('admin1', 'adminpass', '111-111-1111', 'Admin Address', 'Admin', NULL) ON CONFLICT (login) DO NOTHING;
INSERT INTO users (login, password, phone_num, address, role, favorite_category) VALUES ('seller1', 'sellerpass', '222-222-2222', 'Seller Address', 'Seller', 'Electronics') ON CONFLICT (login) DO NOTHING;
INSERT INTO users (login, password, phone_num, address, role, favorite_category) VALUES ('buyer1', 'buyerpass', '333-333-3333', 'Buyer Address', 'Buyer', 'Electronics') ON CONFLICT (login) DO NOTHING;
INSERT INTO users (login, password, phone_num, address, role, favorite_category) VALUES ('buyer2', 'buyerpass', '444-444-4444', 'Buyer 2 Address', 'Buyer', 'Books') ON CONFLICT (login) DO NOTHING;

-- Required demo item
INSERT INTO item (item_id, item_name, category, starting_price, image_url, item_condition, description, seller_login, seller_role) VALUES (9001, 'MacBook Pro', 'Electronics', 700.00, NULL, 'Used', '2021 MacBook Pro', 'seller1', 'Seller') ON CONFLICT (item_id) DO NOTHING;

-- Required demo auction
INSERT INTO auction (auction_id, item_id, seller_login, seller_role, current_highest_bid, auction_status, winner_login, winner_role) VALUES (9001, 9001, 'seller1', 'Seller', 700.00, 'Active', NULL, 'Buyer') ON CONFLICT (auction_id) DO NOTHING;

-- Login Check
SELECT login, role FROM users WHERE login = 'buyer1' AND password = 'buyerpass';

-- Browse Active Auctions
SELECT a.auction_id, i.item_name, i.category, i.description, i.item_condition, a.current_highest_bid, a.auction_status, a.seller_login FROM auction a JOIN item i ON a.item_id = i.item_id WHERE a.auction_status = 'Active';

-- Search Auctions by Category
SELECT a.auction_id, i.item_name, i.category, a.current_highest_bid, a.auction_status FROM auction a JOIN item i ON a.item_id = i.item_id WHERE a.auction_status = 'Active' AND i.category = 'Electronics';

-- Search Auctions by Item Name
SELECT a.auction_id, i.item_name, i.category, a.current_highest_bid, a.auction_status FROM auction a JOIN item i ON a.item_id = i.item_id WHERE LOWER(i.item_name) LIKE LOWER('%macbook%');

-- View Auction Details
SELECT a.auction_id, i.item_name, i.category, i.description, i.item_condition, i.starting_price, a.current_highest_bid, a.auction_status, a.seller_login FROM auction a JOIN item i ON a.item_id = i.item_id WHERE a.auction_id = 9001;

-- View All Bids for an Auction
SELECT bid_id, buyer_login, bid_amount, bid_timestamp FROM bid WHERE auction_id = 9001 ORDER BY bid_amount DESC;

-- View Highest Bidder
SELECT buyer_login, bid_amount FROM bid WHERE auction_id = 9001 ORDER BY bid_amount DESC LIMIT 1;

-- Seller's Auctions
SELECT a.auction_id, i.item_name, a.current_highest_bid, a.auction_status FROM auction a JOIN item i ON a.item_id = i.item_id WHERE a.seller_login = 'seller1';

-- Auctions Won by Buyer
SELECT a.auction_id, i.item_name, a.current_highest_bid FROM auction a JOIN item i ON a.item_id = i.item_id WHERE a.winner_login = 'buyer1';

-- Place Bid Safely
INSERT INTO bid (bid_id, auction_id, buyer_login, buyer_role, bid_amount) SELECT 9001, auction_id, 'buyer1', 'Buyer', 750.00 FROM auction WHERE auction_id = 9001 AND auction_status = 'Active' AND seller_login <> 'buyer1' AND 750.00 > current_highest_bid ON CONFLICT (bid_id) DO NOTHING;

-- Update Current Highest Bid Safely
UPDATE auction SET current_highest_bid = 750.00 WHERE auction_id = 9001 AND auction_status = 'Active' AND seller_login <> 'buyer1' AND 750.00 > current_highest_bid;

-- View All Bids After Insert
SELECT bid_id, buyer_login, bid_amount, bid_timestamp FROM bid WHERE auction_id = 9001 ORDER BY bid_amount DESC;

-- Close Auction
UPDATE auction SET auction_status = 'Closed', winner_login = (SELECT buyer_login FROM bid WHERE auction_id = 9001 ORDER BY bid_amount DESC, bid_timestamp ASC LIMIT 1), winner_role = 'Buyer' WHERE auction_id = 9001 AND auction_status = 'Active';

-- View Closed Auction
SELECT auction_id, item_id, seller_login, current_highest_bid, auction_status, winner_login FROM auction WHERE auction_id = 9001;

-- Create Payment
INSERT INTO payment (payment_id, auction_id, buyer_login, buyer_role, amount, payment_status) SELECT 9001, auction_id, winner_login, 'Buyer', current_highest_bid, 'Pending' FROM auction WHERE auction_id = 9001 AND auction_status = 'Closed' AND winner_login IS NOT NULL ON CONFLICT (payment_id) DO NOTHING;

-- Complete Payment
UPDATE payment SET payment_status = 'Completed' WHERE payment_id = 9001;

-- Create Shipment
INSERT INTO shipment (shipment_id, auction_id, address, shipment_status, tracking_number) SELECT 9001, p.auction_id, u.address, 'Pending', NULL FROM payment p JOIN users u ON p.buyer_login = u.login WHERE p.payment_id = 9001 AND p.payment_status = 'Completed' ON CONFLICT (shipment_id) DO NOTHING;

-- Mark Shipment Shipped
UPDATE shipment SET shipment_status = 'Shipped', tracking_number = 'TRACK123456' WHERE shipment_id = 9001;

-- Mark Shipment Delivered
UPDATE shipment SET shipment_status = 'Delivered' WHERE shipment_id = 9001;

-- Admin View All Users
SELECT login, phone_num, role, address, favorite_category FROM users ORDER BY login;

-- Admin View All Active Auctions
SELECT a.auction_id, i.item_name, a.seller_login, a.current_highest_bid, a.auction_status FROM auction a JOIN item i ON a.item_id = i.item_id WHERE a.auction_status = 'Active';

-- Admin View Payments
SELECT payment_id, auction_id, buyer_login, amount, payment_status FROM payment ORDER BY payment_id;

-- Admin View Shipments
SELECT shipment_id, auction_id, shipment_status, tracking_number FROM shipment ORDER BY shipment_id;

-- Report: Active auctions by category
SELECT i.category, COUNT(*) AS active_auction_count FROM auction a JOIN item i ON a.item_id = i.item_id WHERE a.auction_status = 'Active' GROUP BY i.category ORDER BY i.category;

-- Report: Total bids by buyer
SELECT buyer_login, COUNT(*) AS total_bids, MAX(bid_amount) AS highest_bid FROM bid GROUP BY buyer_login ORDER BY buyer_login;

-- Report: Auctions by seller
SELECT seller_login, COUNT(*) AS total_auctions FROM auction GROUP BY seller_login ORDER BY seller_login;

-- Report: Payments by status
SELECT payment_status, COUNT(*) AS payment_count FROM payment GROUP BY payment_status ORDER BY payment_status;
