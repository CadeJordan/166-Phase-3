from data import mock_data


def get_categories():
    """SQL: SELECT DISTINCT category FROM item ORDER BY category."""
    return mock_data.CATEGORIES


def get_all_users():
    """SQL: SELECT login, phone_num, address, role, favorite_category FROM users."""
    return mock_data.USERS


def get_all_items():
    """SQL: SELECT * FROM item."""
    return mock_data.ITEMS


def get_user(login):
    """SQL: SELECT * FROM users WHERE login = %s."""
    return mock_data.get_user(login)


def get_item(item_id):
    """SQL: SELECT * FROM item WHERE item_id = %s."""
    return mock_data.get_item(item_id)


def get_auction_with_item(auction_id):
    """SQL: JOIN auction + item for a single auction_id."""
    return mock_data.get_auction_with_item(auction_id)


def get_bids_for_auction(auction_id):
    """SQL: SELECT * FROM bid WHERE auction_id = %s ORDER BY bid_timestamp DESC."""
    return mock_data.get_bids_for_auction(auction_id)


def get_payment_for_auction(auction_id):
    """SQL: SELECT * FROM payment WHERE auction_id = %s."""
    return mock_data.get_payment_for_auction(auction_id)


def get_shipment_for_auction(auction_id):
    """SQL: SELECT * FROM shipment WHERE auction_id = %s."""
    return mock_data.get_shipment_for_auction(auction_id)


def search_auctions(q="", category="", status="", sort="newest"):
    """
    SQL: JOIN auction + item with optional filters.
    sort: newest | price_asc | price_desc
    """
    return mock_data.search_auctions(q=q, category=category, status=status, sort=sort)


def get_user_bids(login):
    """SQL: bids by buyer joined with auction + item."""
    return mock_data.get_user_bids(login)


def get_user_wins(login):
    """SQL: closed auctions where winner_login = login, plus payment/shipment."""
    return mock_data.get_user_wins(login)


def get_seller_listings(login):
    """SQL: items by seller joined with auction and bid count."""
    return mock_data.get_seller_listings(login)


def get_all_auctions_enriched():
    """SQL: all auctions joined with item and bid count."""
    return mock_data.get_all_auctions_enriched()


def get_payments(status_filter=""):
    """SQL: payments joined with auction/item, optional status filter."""
    payments = mock_data.PAYMENTS
    if status_filter:
        payments = [p for p in payments if p["payment_status"] == status_filter]
    enriched = []
    for p in payments:
        auction = mock_data.get_auction_with_item(p["auction_id"])
        enriched.append({**p, "auction": auction})
    return enriched


def get_shipments():
    """SQL: shipments joined with auction/item."""
    enriched = []
    for s in mock_data.SHIPMENTS:
        auction = mock_data.get_auction_with_item(s["auction_id"])
        enriched.append({**s, "auction": auction})
    return enriched


def get_admin_stats():
    """SQL: aggregate counts for dashboard cards."""
    return mock_data.get_admin_stats()


def get_seller_hub_stats(login):
    """SQL: active listing count and total bids for seller."""
    listings = mock_data.get_seller_listings(login)
    active = len([l for l in listings if l["auction"] and l["auction"]["auction_status"] == "Active"])
    total_bids = sum(l["bid_count"] for l in listings)
    return {"active_listings": active, "total_bids": total_bids, "listings": listings}


def authenticate_user(login, password):
    """SQL: verify login/password. Return user dict or None."""
    return None  # demo login uses session dropdown instead


def register_user(phone_num, login, password, address, favorite_category=None):
    """SQL: INSERT INTO users (role defaults to Buyer)."""
    raise NotImplementedError("Wire to SQL INSERT users")


def update_user_profile(login, phone_num, address, favorite_category=None):
    """SQL: UPDATE users SET phone_num, address, favorite_category WHERE login = %s."""
    raise NotImplementedError("Wire to SQL UPDATE users")


def place_bid(auction_id, buyer_login, bid_amount):
    """SQL: INSERT bid + UPDATE auction.current_highest_bid with constraints."""
    raise NotImplementedError("Wire to SQL bid transaction")


def create_listing(seller_login, item_name, category, starting_price, **kwargs):
    """SQL: INSERT item + INSERT auction (status Active)."""
    raise NotImplementedError("Wire to SQL create item/auction")


def update_listing(item_id, seller_login, **fields):
    """SQL: UPDATE item WHERE item_id AND seller_login match."""
    raise NotImplementedError("Wire to SQL UPDATE item")


def end_auction(auction_id, seller_login):
    """SQL: set auction_status Closed, set winner_login to highest bidder."""
    raise NotImplementedError("Wire to SQL end auction")


def update_user_role(login, new_role):
    """SQL: UPDATE users SET role — admin only."""
    raise NotImplementedError("Wire to SQL UPDATE users role")


def remove_item(item_id):
    """SQL: DELETE item (admin) with FK checks."""
    raise NotImplementedError("Wire to SQL DELETE item")


def process_payment(auction_id, buyer_login):
    """SQL: INSERT/UPDATE payment status."""
    raise NotImplementedError("Wire to SQL payment")


def update_shipment(shipment_id, shipment_status, tracking_number=None):
    """SQL: UPDATE shipment."""
    raise NotImplementedError("Wire to SQL UPDATE shipment")
