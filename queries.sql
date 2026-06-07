-- Login Check
SELECT login, role FROM users WHERE login = 'buyer1' AND password = 'buyerpass';

-- Browse Active Auctions
SELECT a.auction_id, i.item_name, i.category, i.description, i.item_condition, a.current_highest_bid, a.auction_status, a.seller_login FROM auction a JOIN item i ON a.item_id = i.item_id WHERE a.auction_status = 'Active';

-- Search Auctions by Category
SELECT a.auction_id, i.item_name, i.category, a.current_highest_bid, a.auction_status FROM auction a JOIN item i ON a.item_id = i.item_id WHERE a.auction_status = 'Active' AND i.category = 'Electronics';

-- Search Auctions by Item Name
SELECT a.auction_id, i.item_name, i.category, a.current_highest_bid, a.auction_status FROM auction a JOIN item i ON a.item_id = i.item_id WHERE LOWER(i.item_name) LIKE LOWER('%iphone%');

-- View Auction Details
SELECT a.auction_id, i.item_name, i.category, i.description, i.item_condition, i.starting_price, a.current_highest_bid, a.auction_status, a.seller_login FROM auction a JOIN item i ON a.item_id = i.item_id WHERE a.auction_id = 1;

-- View All Bids for an Auction
SELECT bid_id, buyer_login, bid_amount, bid_timestamp FROM bid WHERE auction_id = 1 ORDER BY bid_amount DESC;

-- View Highest Bidder
SELECT buyer_login, bid_amount FROM bid WHERE auction_id = 1 ORDER BY bid_amount DESC LIMIT 1;

-- Seller's Auctions
SELECT a.auction_id, i.item_name, a.current_highest_bid, a.auction_status FROM auction a JOIN item i ON a.item_id = i.item_id WHERE a.seller_login = 'seller1';

-- Auctions Won by Buyer
SELECT a.auction_id, i.item_name, a.current_highest_bid FROM auction a JOIN item i ON a.item_id = i.item_id WHERE a.winner_login = 'buyer1';

-- Create New Item
INSERT INTO item (item_id, item_name, category, starting_price, image_url, item_condition, description, seller_login, seller_role) VALUES (3, 'MacBook Pro', 'Electronics', 700.00, NULL, 'Used', '2021 MacBook Pro', 'seller1', 'Seller');

-- Create New Auction
INSERT INTO auction (auction_id, item_id, seller_login, seller_role, current_highest_bid, auction_status, winner_login, winner_role) VALUES (3, 3, 'seller1', 'Seller', 700.00, 'Active', NULL, 'Buyer');

-- Place Bid
INSERT INTO bid (bid_id, auction_id, buyer_login, buyer_role, bid_amount) VALUES (1, 3, 'buyer1', 'Buyer', 750.00);

-- Update Current Highest Bid
UPDATE auction SET current_highest_bid = 750.00 WHERE auction_id = 3;

-- Close Auction
UPDATE auction SET auction_status = 'Closed', winner_login = (SELECT buyer_login FROM bid WHERE auction_id = 3 ORDER BY bid_amount DESC, bid_timestamp ASC LIMIT 1), winner_role = 'Buyer' WHERE auction_id = 3;

-- Create Payment
INSERT INTO payment (payment_id, auction_id, buyer_login, buyer_role, amount, payment_status) VALUES (1, 3, 'buyer1', 'Buyer', 750.00, 'Pending');

-- Complete Payment
UPDATE payment SET payment_status = 'Completed' WHERE payment_id = 1;

-- Create Shipment
INSERT INTO shipment (shipment_id, auction_id, address, shipment_status, tracking_number) VALUES (1, 3, '123 Main St Riverside CA', 'Pending', NULL);

-- Mark Shipment Shipped
UPDATE shipment SET shipment_status = 'Shipped', tracking_number = 'TRACK123456' WHERE shipment_id = 1;

-- Mark Shipment Delivered
UPDATE shipment SET shipment_status = 'Delivered' WHERE shipment_id = 1;

-- Admin View All Users
SELECT login, phone_num, role, address, favorite_category FROM users ORDER BY login;

-- Admin View All Active Auctions
SELECT a.auction_id, i.item_name, a.seller_login, a.current_highest_bid, a.auction_status FROM auction a JOIN item i ON a.item_id = i.item_id WHERE a.auction_status = 'Active';

-- Admin View Payments
SELECT payment_id, auction_id, buyer_login, amount, payment_status FROM payment ORDER BY payment_id;

-- Admin View Shipments
SELECT shipment_id, auction_id, shipment_status, tracking_number FROM shipment ORDER BY shipment_id;