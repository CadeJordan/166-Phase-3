\copy users(login,password,phone_num,address,role,favorite_category) FROM 'users.dat' WITH (FORMAT csv);
\copy item(item_id,item_name,category,starting_price,image_url,item_condition,description,seller_login,seller_role) FROM 'item.dat' WITH (FORMAT csv);
\copy auction(auction_id,item_id,seller_login,seller_role,current_highest_bid,auction_status,winner_login,winner_role) FROM 'auction.dat' WITH (FORMAT csv);
\copy bid(bid_id,auction_id,buyer_login,buyer_role,bid_amount,bid_timestamp) FROM 'bid.dat' WITH (FORMAT csv);
\copy payment(payment_id,auction_id,buyer_login,buyer_role,amount,payment_status) FROM 'payment.dat' WITH (FORMAT csv);
\copy shipment(shipment_id,auction_id,address,shipment_status,tracking_number) FROM 'shipment.dat' WITH (FORMAT csv);
