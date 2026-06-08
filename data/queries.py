import sys
from data.EmbeddedSQL import EmbeddedSQL

_esql = None

def configure_db(dbname, dbport, user, passwd=""):
    """Create one shared EmbeddedSQL connection for all query functions."""
    global _esql
    if _esql is not None:
        _esql.cleanup()
    _esql = EmbeddedSQL(dbname, dbport, user, passwd)
    return _esql


def set_esql(esql):
    """Let another file pass in an already-created EmbeddedSQL object."""
    global _esql
    _esql = esql


def cleanup():
    """Close the shared database connection."""
    global _esql
    if _esql is not None:
        _esql.cleanup()
        _esql = None


def _conn():
    if _esql is None:
        raise RuntimeError("Database is not configured. Call configure_db(dbname, dbport, user) first.")
    return _esql._connection


def _fetch_all(query, params=None):
    cursor = _conn().cursor()
    cursor.execute(query, params or ())
    columns = [desc[0] for desc in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    return rows


def _fetch_one(query, params=None):
    rows = _fetch_all(query, params)
    return rows[0] if rows else None


def _execute(query, params=None):
    cursor = _conn().cursor()
    try:
        cursor.execute(query, params or ())
        affected = cursor.rowcount
        _conn().commit()
        return affected
    except Exception:
        _conn().rollback()
        raise
    finally:
        cursor.close()


def _next_id(table_name, column_name):
    # table/column names are constants passed by this file only, not user input.
    row = _fetch_one(f"SELECT COALESCE(MAX({column_name}), 0) + 1 AS next_id FROM {table_name};")
    return row["next_id"]

# cursor = _conn().cursor()
#     try:
#         for query, params in statements:
#             cursor.execute(query, params)
#         _conn().commit()
#         return True
#     except Exception:
#         _conn().rollback()
#         raise
#     finally:
#         cursor.close()


def get_categories():
    """SQL: SELECT DISTINCT category FROM item ORDER BY category."""
    rows = _fetch_all("SELECT DISTINCT category FROM item ORDER BY category;")
    return [row["category"] for row in rows]


def get_all_users():
    """SQL: SELECT login, phone_num, address, role, favorite_category FROM users."""
    return _fetch_all("SELECT login, phone_num, address, role, favorite_category FROM users ORDER BY login;")


def get_all_items():
    """SQL: SELECT * FROM item."""
    return _fetch_all("SELECT item_id, item_name, category, starting_price, image_url, item_condition, description, seller_login, seller_role FROM item ORDER BY item_id;")


def get_user(login):
    """SQL: SELECT * FROM users WHERE login = %s."""
    return _fetch_one("SELECT login, password, phone_num, address, role, favorite_category FROM users WHERE login = %s;", (login,))


def get_item(item_id):
    """SQL: SELECT * FROM item WHERE item_id = %s."""
    return _fetch_one("SELECT item_id, item_name, category, starting_price, image_url, item_condition, description, seller_login, seller_role FROM item WHERE item_id = %s;", (item_id,))


def get_auction_with_item(auction_id):
    """SQL: JOIN auction + item for a single auction_id."""
    return _fetch_one(
        "SELECT a.auction_id, a.item_id, a.seller_login, a.seller_role, a.current_highest_bid, a.auction_status, a.winner_login, a.winner_role, i.item_name, i.category, i.starting_price, i.image_url, i.item_condition, i.description FROM auction a JOIN item i ON a.item_id = i.item_id WHERE a.auction_id = %s;",
        (auction_id,)
    )


def get_bids_for_auction(auction_id):
    """SQL: SELECT * FROM bid WHERE auction_id = %s ORDER BY bid_timestamp DESC."""
    return _fetch_all("SELECT bid_id, auction_id, buyer_login, buyer_role, bid_amount, bid_timestamp FROM bid WHERE auction_id = %s ORDER BY bid_timestamp DESC;", (auction_id,))


def get_payment_for_auction(auction_id):
    """SQL: SELECT * FROM payment WHERE auction_id = %s."""
    return _fetch_one("SELECT payment_id, auction_id, buyer_login, buyer_role, amount, payment_status FROM payment WHERE auction_id = %s;", (auction_id,))


def get_shipment_for_auction(auction_id):
    """SQL: SELECT * FROM shipment WHERE auction_id = %s."""
    return _fetch_one("SELECT shipment_id, auction_id, address, shipment_status, tracking_number FROM shipment WHERE auction_id = %s;", (auction_id,))


def search_auctions(q="", category="", status="", sort="newest"):
    """
    SQL: JOIN auction + item with optional filters.
    sort: newest | price_asc | price_desc
    """
    where = []
    params = []

    if q:
        where.append("LOWER(i.item_name) LIKE LOWER(%s)")
        params.append(f"%{q}%")
    if category:
        where.append("i.category = %s")
        params.append(category)
    if status:
        where.append("a.auction_status = %s")
        params.append(status)

    order_by = "a.auction_id DESC"
    if sort == "price_asc":
        order_by = "a.current_highest_bid ASC"
    elif sort == "price_desc":
        order_by = "a.current_highest_bid DESC"

    sql = "SELECT a.auction_id, a.item_id, a.seller_login, a.current_highest_bid, a.auction_status, a.winner_login, i.item_name, i.category, i.description, i.item_condition, i.starting_price, i.image_url FROM auction a JOIN item i ON a.item_id = i.item_id"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += f" ORDER BY {order_by};"

    return _fetch_all(sql, tuple(params))


def get_user_bids(login):
    """SQL: bids by buyer joined with auction + item."""
    return _fetch_all(
        "SELECT b.bid_id, b.auction_id, b.buyer_login, b.bid_amount, b.bid_timestamp, a.auction_status, a.current_highest_bid, i.item_name, i.category FROM bid b JOIN auction a ON b.auction_id = a.auction_id JOIN item i ON a.item_id = i.item_id WHERE b.buyer_login = %s ORDER BY b.bid_timestamp DESC;",
        (login,)
    )


def get_user_wins(login):
    """SQL: closed auctions where winner_login = login, plus payment/shipment."""
    return _fetch_all(
        "SELECT a.auction_id, a.current_highest_bid, a.auction_status, a.winner_login, i.item_name, i.category, p.payment_id, p.payment_status, s.shipment_id, s.shipment_status, s.tracking_number FROM auction a JOIN item i ON a.item_id = i.item_id LEFT JOIN payment p ON a.auction_id = p.auction_id LEFT JOIN shipment s ON a.auction_id = s.auction_id WHERE a.auction_status = 'Closed' AND a.winner_login = %s ORDER BY a.auction_id DESC;",
        (login,)
    )


def get_seller_listings(login):
    """SQL: items by seller joined with auction and bid count."""
    return _fetch_all(
        "SELECT i.item_id, i.item_name, i.category, i.starting_price, i.image_url, i.item_condition, i.description, a.auction_id, a.current_highest_bid, a.auction_status, a.winner_login, COUNT(b.bid_id) AS bid_count FROM item i LEFT JOIN auction a ON i.item_id = a.item_id LEFT JOIN bid b ON a.auction_id = b.auction_id WHERE i.seller_login = %s GROUP BY i.item_id, i.item_name, i.category, i.starting_price, i.image_url, i.item_condition, i.description, a.auction_id, a.current_highest_bid, a.auction_status, a.winner_login ORDER BY i.item_id DESC;",
        (login,)
    )


def get_all_auctions_enriched():
    """SQL: all auctions joined with item and bid count."""
    return _fetch_all(
        "SELECT a.auction_id, a.item_id, a.seller_login, a.current_highest_bid, a.auction_status, a.winner_login, i.item_name, i.category, i.description, i.item_condition, COUNT(b.bid_id) AS bid_count FROM auction a JOIN item i ON a.item_id = i.item_id LEFT JOIN bid b ON a.auction_id = b.auction_id GROUP BY a.auction_id, a.item_id, a.seller_login, a.current_highest_bid, a.auction_status, a.winner_login, i.item_name, i.category, i.description, i.item_condition ORDER BY a.auction_id DESC;"
    )


# def get_payments(status_filter=""):
#     """SQL: payments joined with auction/item, optional status filter."""
#     payments = mock_data.PAYMENTS
#     if status_filter:
#         payments = [p for p in payments if p["payment_status"] == status_filter]
#     enriched = []
#     for p in payments:
#         auction = mock_data.get_auction_with_item(p["auction_id"])
#         enriched.append({**p, "auction": auction})
#     return enriched
def get_payments(status_filter=""):
    """SQL: payments joined with auction/item, optional status filter."""
    if status_filter:
        return _fetch_all(
            "SELECT p.payment_id, p.auction_id, p.buyer_login, p.amount, p.payment_status, i.item_name, i.category FROM payment p JOIN auction a ON p.auction_id = a.auction_id JOIN item i ON a.item_id = i.item_id WHERE p.payment_status = %s ORDER BY p.payment_id;",
            (status_filter,)
        )
    return _fetch_all(
        "SELECT p.payment_id, p.auction_id, p.buyer_login, p.amount, p.payment_status, i.item_name, i.category FROM payment p JOIN auction a ON p.auction_id = a.auction_id JOIN item i ON a.item_id = i.item_id ORDER BY p.payment_id;"
    )


# def get_shipments():
#     """SQL: shipments joined with auction/item."""
#     enriched = []
#     for s in mock_data.SHIPMENTS:
#         auction = mock_data.get_auction_with_item(s["auction_id"])
#         enriched.append({**s, "auction": auction})
#     return enriched

def get_shipments():
    """SQL: shipments joined with auction/item."""
    return _fetch_all(
        "SELECT s.shipment_id, s.auction_id, s.address, s.shipment_status, s.tracking_number, i.item_name, i.category FROM shipment s JOIN auction a ON s.auction_id = a.auction_id JOIN item i ON a.item_id = i.item_id ORDER BY s.shipment_id;"
    )


# def get_admin_stats():
#     """SQL: aggregate counts for dashboard cards."""
#     return mock_data.get_admin_stats()


def get_admin_stats():
    """SQL: aggregate counts for dashboard cards."""
    return {
        "users": _fetch_one("SELECT COUNT(*) AS count FROM users;")["count"],
        "items": _fetch_one("SELECT COUNT(*) AS count FROM item;")["count"],
        "auctions": _fetch_one("SELECT COUNT(*) AS count FROM auction;")["count"],
        "active_auctions": _fetch_one("SELECT COUNT(*) AS count FROM auction WHERE auction_status = 'Active';")["count"],
        "closed_auctions": _fetch_one("SELECT COUNT(*) AS count FROM auction WHERE auction_status = 'Closed';")["count"],
        "bids": _fetch_one("SELECT COUNT(*) AS count FROM bid;")["count"],
        "payments": _fetch_one("SELECT COUNT(*) AS count FROM payment;")["count"],
        "shipments": _fetch_one("SELECT COUNT(*) AS count FROM shipment;")["count"],
    }


# def get_seller_hub_stats(login):
#     """SQL: active listing count and total bids for seller."""
#     listings = mock_data.get_seller_listings(login)
#     active = len([l for l in listings if l["auction"] and l["auction"]["auction_status"] == "Active"])
#     total_bids = sum(l["bid_count"] for l in listings)
#     return {"active_listings": active, "total_bids": total_bids, "listings": listings}

def get_seller_hub_stats(login):
    """SQL: active listing count and total bids for seller."""
    stats = _fetch_one(
        "SELECT COUNT(DISTINCT a.auction_id) FILTER (WHERE a.auction_status = 'Active') AS active_listings, COUNT(b.bid_id) AS total_bids FROM auction a LEFT JOIN bid b ON a.auction_id = b.auction_id WHERE a.seller_login = %s;",
        (login,)
    )
    listings = get_seller_listings(login)
    return {
        "active_listings": stats["active_listings"] if stats else 0,
        "total_bids": stats["total_bids"] if stats else 0,
        "listings": listings,
    }


def authenticate_user(login, password):
    """SQL: verify login/password. Return user dict or None."""
    return _fetch_one("SELECT login, phone_num, address, role, favorite_category FROM users WHERE login = %s AND password = %s;", (login, password))


def register_user(phone_num, login, password, address, favorite_category=None):
    """SQL: INSERT INTO users. New accounts default to Buyer."""
    _execute(
        "INSERT INTO users (login, password, phone_num, address, role, favorite_category) VALUES (%s, %s, %s, %s, 'Buyer', %s);",
        (login, password, phone_num, address, favorite_category)
    )
    return get_user(login)


def update_user_profile(login, phone_num, address, favorite_category=None):
    """SQL: UPDATE users SET phone_num, address, favorite_category WHERE login = %s."""
    _execute(
        "UPDATE users SET phone_num = %s, address = %s, favorite_category = %s WHERE login = %s;",
        (phone_num, address, favorite_category, login)
    )
    return get_user(login)


def place_bid(auction_id, buyer_login, bid_amount):
    """SQL: INSERT bid + UPDATE auction.current_highest_bid with constraints."""
    bid_id = _next_id("bid", "bid_id")
    cursor = _conn().cursor()
    try:
        cursor.execute(
            "INSERT INTO bid (bid_id, auction_id, buyer_login, buyer_role, bid_amount) SELECT %s, auction_id, %s, 'Buyer', %s FROM auction WHERE auction_id = %s AND auction_status = 'Active' AND seller_login <> %s AND %s > current_highest_bid;",
            (bid_id, buyer_login, bid_amount, auction_id, buyer_login, bid_amount)
        )
        inserted = cursor.rowcount
        if inserted == 0:
            _conn().rollback()
            cursor.close()
            return {"success": False, "message": "Bid rejected. Auction must be active, bid must be higher, and seller cannot bid on own auction."}

        cursor.execute(
            "UPDATE auction SET current_highest_bid = %s WHERE auction_id = %s;",
            (bid_amount, auction_id)
        )
        _conn().commit()
        cursor.close()
        return {"success": True, "bid_id": bid_id, "auction_id": auction_id, "bid_amount": bid_amount}
    except Exception as e:
        _conn().rollback()
        cursor.close()
        raise e


def create_listing(seller_login, item_name, category, starting_price, **kwargs):
    """SQL: INSERT item + INSERT auction with status Active."""
    item_id = kwargs.get("item_id") or _next_id("item", "item_id")
    auction_id = kwargs.get("auction_id") or _next_id("auction", "auction_id")
    image_url = kwargs.get("image_url")
    item_condition = kwargs.get("item_condition") or kwargs.get("condition")
    description = kwargs.get("description")

    cursor = _conn().cursor()
    try:
        cursor.execute(
            "INSERT INTO item (item_id, item_name, category, starting_price, image_url, item_condition, description, seller_login, seller_role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Seller');",
            (item_id, item_name, category, starting_price, image_url, item_condition, description, seller_login)
        )
        cursor.execute(
            "INSERT INTO auction (auction_id, item_id, seller_login, seller_role, current_highest_bid, auction_status, winner_login, winner_role) VALUES (%s, %s, %s, 'Seller', %s, 'Active', NULL, 'Buyer');",
            (auction_id, item_id, seller_login, starting_price)
        )
        _conn().commit()
        cursor.close()
        return get_auction_with_item(auction_id)
    except Exception as e:
        _conn().rollback()
        cursor.close()
        raise e


def update_listing(item_id, seller_login, **fields):
    """SQL: UPDATE item WHERE item_id AND seller_login match."""
    allowed = {
        "item_name": "item_name",
        "category": "category",
        "starting_price": "starting_price",
        "image_url": "image_url",
        "item_condition": "item_condition",
        "condition": "item_condition",
        "description": "description",
    }

    assignments = []
    params = []
    for key, value in fields.items():
        if key in allowed:
            assignments.append(f"{allowed[key]} = %s")
            params.append(value)

    if not assignments:
        return get_item(item_id)

    params.extend([item_id, seller_login])
    _execute(
        f"UPDATE item SET {', '.join(assignments)} WHERE item_id = %s AND seller_login = %s;",
        tuple(params)
    )
    return get_item(item_id)


def end_auction(auction_id, seller_login):
    """SQL: set auction_status Closed, set winner_login to highest bidder."""
    _execute(
        "UPDATE auction SET auction_status = 'Closed', winner_login = (SELECT buyer_login FROM bid WHERE auction_id = %s ORDER BY bid_amount DESC, bid_timestamp ASC LIMIT 1), winner_role = 'Buyer' WHERE auction_id = %s AND seller_login = %s AND auction_status = 'Active';",
        (auction_id, auction_id, seller_login)
    )
    return get_auction_with_item(auction_id)


def update_user_role(login, new_role):
    """SQL: UPDATE users SET role — admin only in app/front-end logic."""
    _execute("UPDATE users SET role = %s WHERE login = %s;", (new_role, login))
    return get_user(login)


def remove_item(item_id):
    """SQL: DELETE item. FK constraints may prevent deleting active/referenced items."""
    return _execute("DELETE FROM item WHERE item_id = %s;", (item_id,))


def process_payment(auction_id, buyer_login):
    """SQL: INSERT payment for a closed won auction or mark existing payment completed."""
    existing = get_payment_for_auction(auction_id)
    if existing:
        _execute(
            "UPDATE payment SET payment_status = 'Completed' WHERE auction_id = %s AND buyer_login = %s;",
            (auction_id, buyer_login)
        )
        return get_payment_for_auction(auction_id)

    payment_id = _next_id("payment", "payment_id")
    _execute(
        "INSERT INTO payment (payment_id, auction_id, buyer_login, buyer_role, amount, payment_status) SELECT %s, auction_id, winner_login, 'Buyer', current_highest_bid, 'Completed' FROM auction WHERE auction_id = %s AND auction_status = 'Closed' AND winner_login = %s;",
        (payment_id, auction_id, buyer_login)
    )
    return get_payment_for_auction(auction_id)


def update_shipment(shipment_id, shipment_status, tracking_number=None):
    """SQL: UPDATE shipment."""
    _execute(
        "UPDATE shipment SET shipment_status = %s, tracking_number = %s WHERE shipment_id = %s;",
        (shipment_status, tracking_number, shipment_id)
    )
    return _fetch_one("SELECT shipment_id, auction_id, address, shipment_status, tracking_number FROM shipment WHERE shipment_id = %s;", (shipment_id,))