CREATE INDEX IF NOT EXISTS itemCategory ON item(category);
CREATE INDEX IF NOT EXISTS auctionStatus ON auction(auction_status);
CREATE INDEX IF NOT EXISTS auctionSeller ON auction(seller_login);
CREATE INDEX IF NOT EXISTS bidAuction ON bid(auction_id);
CREATE INDEX IF NOT EXISTS bidBuyer ON bid(buyer_login);
CREATE INDEX IF NOT EXISTS payStatus ON payment(payment_status);
CREATE INDEX IF NOT EXISTS shipStatus ON shipment(shipment_status);