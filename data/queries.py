from data.db_connection import DB_CONFIG, EmbeddedSQL


def configure_db(dbname, dbport, user, passwd=""):
    DB_CONFIG["dbname"] = dbname
    DB_CONFIG["dbport"] = str(dbport)
    DB_CONFIG["user"] = user
    DB_CONFIG["passwd"] = passwd


def cleanup():
    pass


def _connect():
    if not DB_CONFIG["dbname"] or not DB_CONFIG["user"]:
        raise RuntimeError("Database is not configured. Call configure_db() first.")
    return EmbeddedSQL(DB_CONFIG["dbname"], DB_CONFIG["dbport"], DB_CONFIG["user"], DB_CONFIG["passwd"])


def _fetch_all(query, params=None):
    esql = _connect()
    try:
        return esql.execute_query(query, params)
    finally:
        esql.cleanup()


def _fetch_one(query, params=None):
    esql = _connect()
    try:
        return esql.execute_one(query, params)
    finally:
        esql.cleanup()


def _execute(sql, params=None):
    esql = _connect()
    try:
        return esql.execute_update(sql, params)
    finally:
        esql.cleanup()


# Templates expect nested dicts (e.g. auction.item.item_name), but the SQL returns flat rows, so these helpers reshape them

def _shape_item(row):
    return {
        "item_id": row.get("item_id"),
        "item_name": row.get("item_name"),
        "category": row.get("category"),
        "starting_price": row.get("starting_price"),
        "image_url": row.get("image_url"),
        "item_condition": row.get("item_condition"),
        "description": row.get("description"),
    }


def _shape_auction(row):
    if row is None:
        return None
    shaped = dict(row)
    shaped["item"] = _shape_item(row)
    return shaped


def get_all_users():
    return _fetch_all("SELECT login, phone_num, address, role, favorite_category FROM users ORDER BY login;")


def get_all_items():
    return _fetch_all("SELECT item_id, item_name, category, starting_price, image_url, item_condition, description, seller_login, seller_role FROM item ORDER BY item_id;")


def get_user(login):
    return _fetch_one("SELECT login, phone_num, address, role, favorite_category FROM users WHERE login = %s;", (login,))


def authenticate_user(login, password):
    # Returns the user row only if the login/password pair matches.
    return _fetch_one("SELECT login, phone_num, address, role, favorite_category FROM users WHERE login = %s AND password = %s;", (login, password))


def get_item(item_id):
    return _fetch_one("SELECT item_id, item_name, category, starting_price, image_url, item_condition, description, seller_login, seller_role FROM item WHERE item_id = %s;", (item_id,))


def get_auction_with_item(auction_id):
    return _shape_auction(_fetch_one("SELECT a.auction_id, a.item_id, i.item_name, i.category, i.description, i.item_condition, i.starting_price, a.current_highest_bid, a.auction_status, a.seller_login, a.winner_login FROM auction a JOIN item i ON a.item_id = i.item_id WHERE a.auction_id = %s;", (auction_id,)))


def get_bids_for_auction(auction_id):
    return _fetch_all("SELECT bid_id, auction_id, buyer_login, buyer_role, bid_amount, bid_timestamp FROM bid WHERE auction_id = %s ORDER BY bid_amount DESC, bid_timestamp ASC;", (auction_id,))


def get_payment_for_auction(auction_id):
    return _fetch_one("SELECT payment_id, auction_id, buyer_login, buyer_role, amount, payment_status FROM payment WHERE auction_id = %s;", (auction_id,))


def get_shipment_for_auction(auction_id):
    return _fetch_one("SELECT shipment_id, auction_id, address, shipment_status, tracking_number FROM shipment WHERE auction_id = %s;", (auction_id,))


def search_auctions(q="", category="", status="", sort="newest"):
    sql = "SELECT a.auction_id, i.item_name, i.category, i.description, i.item_condition, a.current_highest_bid, a.auction_status, a.seller_login FROM auction a JOIN item i ON a.item_id = i.item_id WHERE 1=1"
    params = []

    if q:
        sql += " AND (LOWER(i.item_name) LIKE LOWER(%s) OR LOWER(i.description) LIKE LOWER(%s))"
        params.extend([f"%{q}%", f"%{q}%"])
    if category:
        sql += " AND i.category = %s"
        params.append(category)
    if status:
        sql += " AND a.auction_status = %s"
        params.append(status)

    if sort == "price_asc":
        sql += " ORDER BY a.current_highest_bid ASC;"
    elif sort == "price_desc":
        sql += " ORDER BY a.current_highest_bid DESC;"
    else:
        sql += " ORDER BY a.auction_id DESC;"

    return [_shape_auction(r) for r in _fetch_all(sql, tuple(params))]


def get_user_bids(login):
    rows = _fetch_all("SELECT b.bid_id, b.auction_id, b.bid_amount, b.bid_timestamp, i.item_name, i.category, a.auction_status, a.current_highest_bid FROM bid b JOIN auction a ON b.auction_id = a.auction_id JOIN item i ON a.item_id = i.item_id WHERE b.buyer_login = %s ORDER BY b.bid_timestamp DESC;", (login,))
    return [
        {
            "bid_id": r["bid_id"],
            "auction_id": r["auction_id"],
            "bid_amount": r["bid_amount"],
            "bid_timestamp": r["bid_timestamp"],
            "auction": {
                "auction_id": r["auction_id"],
                "current_highest_bid": r["current_highest_bid"],
                "auction_status": r["auction_status"],
                "item": {"item_name": r["item_name"], "category": r["category"]},
            },
        }
        for r in rows
    ]


def get_user_wins(login):
    rows = _fetch_all("SELECT a.auction_id, i.item_name, i.category, a.current_highest_bid, p.payment_status, s.shipment_status, s.tracking_number FROM auction a JOIN item i ON a.item_id = i.item_id LEFT JOIN payment p ON a.auction_id = p.auction_id LEFT JOIN shipment s ON a.auction_id = s.auction_id WHERE a.winner_login = %s AND a.auction_status = 'Closed' ORDER BY a.auction_id DESC;", (login,))
    return [_shape_auction(r) for r in rows]


def get_seller_listings(login):
    rows = _fetch_all("SELECT i.item_id, i.item_name, i.category, i.starting_price, i.item_condition, i.description, a.auction_id, a.current_highest_bid, a.auction_status, COUNT(b.bid_id) AS bid_count FROM item i LEFT JOIN auction a ON i.item_id = a.item_id LEFT JOIN bid b ON a.auction_id = b.auction_id WHERE i.seller_login = %s GROUP BY i.item_id, i.item_name, i.category, i.starting_price, i.item_condition, i.description, a.auction_id, a.current_highest_bid, a.auction_status ORDER BY i.item_id DESC;", (login,))
    listings = []
    for r in rows:
        auction = None
        if r.get("auction_id") is not None:
            auction = {
                "auction_id": r["auction_id"],
                "current_highest_bid": r["current_highest_bid"],
                "auction_status": r["auction_status"],
            }
        listings.append({"item": _shape_item(r), "auction": auction, "bid_count": r.get("bid_count", 0)})
    return listings


def get_all_auctions_enriched():
    rows = _fetch_all("SELECT a.auction_id, i.item_name, i.category, a.seller_login, a.current_highest_bid, a.auction_status, a.winner_login, COUNT(b.bid_id) AS bid_count FROM auction a JOIN item i ON a.item_id = i.item_id LEFT JOIN bid b ON a.auction_id = b.auction_id GROUP BY a.auction_id, i.item_name, i.category, a.seller_login, a.current_highest_bid, a.auction_status, a.winner_login ORDER BY a.auction_id DESC;")
    return [_shape_auction(r) for r in rows]


def get_payments(status_filter=""):
    if status_filter:
        rows = _fetch_all("SELECT p.payment_id, p.auction_id, p.buyer_login, p.amount, p.payment_status, i.item_name FROM payment p JOIN auction a ON p.auction_id = a.auction_id JOIN item i ON a.item_id = i.item_id WHERE p.payment_status = %s ORDER BY p.payment_id;", (status_filter,))
    else:
        rows = _fetch_all("SELECT p.payment_id, p.auction_id, p.buyer_login, p.amount, p.payment_status, i.item_name FROM payment p JOIN auction a ON p.auction_id = a.auction_id JOIN item i ON a.item_id = i.item_id ORDER BY p.payment_id;")
    return [{**r, "auction": {"item": {"item_name": r["item_name"]}}} for r in rows]


def get_shipments():
    rows = _fetch_all("SELECT s.shipment_id, s.auction_id, s.address, s.shipment_status, s.tracking_number, i.item_name FROM shipment s JOIN auction a ON s.auction_id = a.auction_id JOIN item i ON a.item_id = i.item_id ORDER BY s.shipment_id;")
    return [{**r, "auction": {"item": {"item_name": r["item_name"]}}} for r in rows]


def get_admin_stats():
    return _fetch_one("SELECT (SELECT COUNT(*) FROM users) AS total_users, (SELECT COUNT(*) FROM item) AS total_items, (SELECT COUNT(*) FROM auction WHERE auction_status = 'Active') AS active_auctions, (SELECT COUNT(*) FROM auction WHERE auction_status = 'Closed') AS closed_auctions, (SELECT COUNT(*) FROM bid) AS total_bids, (SELECT COUNT(*) FROM payment) AS total_payments, (SELECT COUNT(*) FROM shipment) AS total_shipments;")


def get_seller_hub_stats(login):
    stats = _fetch_one("SELECT COUNT(DISTINCT a.auction_id) FILTER (WHERE a.auction_status = 'Active') AS active_listings, COUNT(b.bid_id) AS total_bids FROM item i LEFT JOIN auction a ON i.item_id = a.item_id LEFT JOIN bid b ON a.auction_id = b.auction_id WHERE i.seller_login = %s;", (login,))
    if stats is None:
        stats = {"active_listings": 0, "total_bids": 0}
    stats["listings"] = get_seller_listings(login)
    return stats


def register_user(phone_num, login, password, address, favorite_category=None):
    # New accounts always start as Buyer
    return _execute("INSERT INTO users (login, password, phone_num, address, role, favorite_category) VALUES (%s, %s, %s, %s, 'Buyer', %s);", (login, password, phone_num, address, favorite_category))


def update_user_profile(login, phone_num, address, favorite_category=None):
    return _execute("UPDATE users SET phone_num = %s, address = %s, favorite_category = %s WHERE login = %s;", (phone_num, address, favorite_category, login))


def place_bid(auction_id, buyer_login, bid_amount):
    # Insert a bid and raise the highest bid, but only if the bid is valid
    esql = _connect()
    try:
        cursor = esql._connection.cursor()
        cursor.execute("SELECT COALESCE(MAX(bid_id), 0) + 1 FROM bid;")
        bid_id = cursor.fetchone()[0]
        #  Active auction, not the seller, and higher than current
        cursor.execute(
            "INSERT INTO bid (bid_id, auction_id, buyer_login, buyer_role, bid_amount) "
            "SELECT %s, auction_id, %s, 'Buyer', %s FROM auction "
            "WHERE auction_id = %s AND auction_status = 'Active' AND seller_login <> %s AND %s > current_highest_bid;",
            (bid_id, buyer_login, bid_amount, auction_id, buyer_login, bid_amount),
        )
        inserted = cursor.rowcount
        if inserted == 1:
            cursor.execute("UPDATE auction SET current_highest_bid = %s WHERE auction_id = %s;", (bid_amount, auction_id))
        esql._connection.commit()
        cursor.close()
        return inserted == 1
    except Exception:
        esql._connection.rollback()
        raise
    finally:
        esql.cleanup()


def create_listing(seller_login, item_name, category, starting_price, image_url=None, item_condition=None, description=None, **kwargs):
    esql = _connect()
    try:
        cursor = esql._connection.cursor()
        cursor.execute("SELECT COALESCE(MAX(item_id), 0) + 1 FROM item;")
        item_id = cursor.fetchone()[0]
        cursor.execute("SELECT COALESCE(MAX(auction_id), 0) + 1 FROM auction;")
        auction_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO item (item_id, item_name, category, starting_price, image_url, item_condition, description, seller_login, seller_role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Seller');",
            (item_id, item_name, category, starting_price, image_url, item_condition, description, seller_login),
        )
        cursor.execute(
            "INSERT INTO auction (auction_id, item_id, seller_login, seller_role, current_highest_bid, auction_status, winner_login, winner_role) VALUES (%s, %s, %s, 'Seller', %s, 'Active', NULL, 'Buyer');",
            (auction_id, item_id, seller_login, starting_price),
        )
        esql._connection.commit()
        cursor.close()
        return {"item_id": item_id, "auction_id": auction_id}
    except Exception:
        esql._connection.rollback()
        raise
    finally:
        esql.cleanup()


def update_listing(item_id, seller_login, **fields):
    allowed = ["item_name", "category", "starting_price", "image_url", "item_condition", "description"]
    updates = []
    params = []
    for key in allowed:
        if key in fields:
            updates.append(f"{key} = %s")
            params.append(fields[key])
    if not updates:
        return 0
    params.extend([item_id, seller_login])
    return _execute(f"UPDATE item SET {', '.join(updates)} WHERE item_id = %s AND seller_login = %s;", tuple(params))


def end_auction(auction_id, seller_login):
    # Close the auction and set the winner to the highest bidder
    return _execute("UPDATE auction SET auction_status = 'Closed', winner_login = (SELECT buyer_login FROM bid WHERE auction_id = %s ORDER BY bid_amount DESC, bid_timestamp ASC LIMIT 1), winner_role = 'Buyer' WHERE auction_id = %s AND seller_login = %s AND auction_status = 'Active';", (auction_id, auction_id, seller_login))


def update_user_role(login, new_role):
    return _execute("UPDATE users SET role = %s WHERE login = %s;", (new_role, login))


def remove_item(item_id):
    # Fails if an auction still references the item
    return _execute("DELETE FROM item WHERE item_id = %s;", (item_id,))


def process_payment(auction_id, buyer_login):
    esql = _connect()
    try:
        cursor = esql._connection.cursor()
        cursor.execute("SELECT payment_id FROM payment WHERE auction_id = %s;", (auction_id,))
        existing = cursor.fetchone()
        if existing:
            cursor.execute("UPDATE payment SET payment_status = 'Completed' WHERE auction_id = %s AND buyer_login = %s;", (auction_id, buyer_login))
            affected = cursor.rowcount
        else:
            cursor.execute("SELECT COALESCE(MAX(payment_id), 0) + 1 FROM payment;")
            payment_id = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO payment (payment_id, auction_id, buyer_login, buyer_role, amount, payment_status) "
                "SELECT %s, auction_id, %s, 'Buyer', current_highest_bid, 'Completed' FROM auction "
                "WHERE auction_id = %s AND auction_status = 'Closed' AND winner_login = %s;",
                (payment_id, buyer_login, auction_id, buyer_login),
            )
            affected = cursor.rowcount

        # Once paid, create the shipment using the buyer's address (if not already there).
        if affected:
            cursor.execute("SELECT shipment_id FROM shipment WHERE auction_id = %s;", (auction_id,))
            if cursor.fetchone() is None:
                cursor.execute("SELECT address FROM users WHERE login = %s;", (buyer_login,))
                addr_row = cursor.fetchone()
                address = addr_row[0] if addr_row else "Address on file"
                cursor.execute("SELECT COALESCE(MAX(shipment_id), 0) + 1 FROM shipment;")
                shipment_id = cursor.fetchone()[0]
                cursor.execute(
                    "INSERT INTO shipment (shipment_id, auction_id, address, shipment_status, tracking_number) "
                    "VALUES (%s, %s, %s, 'Pending', NULL);",
                    (shipment_id, auction_id, address),
                )
        esql._connection.commit()
        cursor.close()
        return affected
    except Exception:
        esql._connection.rollback()
        raise
    finally:
        esql.cleanup()


def create_shipment(auction_id, address, shipment_status="Pending", tracking_number=None):
    shipment_id = _next_id("shipment", "shipment_id")
    return _execute("INSERT INTO shipment (shipment_id, auction_id, address, shipment_status, tracking_number) VALUES (%s, %s, %s, %s, %s);", (shipment_id, auction_id, address, shipment_status, tracking_number))


def update_shipment(shipment_id, shipment_status, tracking_number=None):
    return _execute("UPDATE shipment SET shipment_status = %s, tracking_number = %s WHERE shipment_id = %s;", (shipment_status, tracking_number, shipment_id))

def report_active_auctions_by_category():
    return _fetch_all("SELECT i.category, COUNT(*) AS active_auction_count FROM auction a JOIN item i ON a.item_id = i.item_id WHERE a.auction_status = 'Active' GROUP BY i.category ORDER BY i.category;")


def report_total_bids_by_buyer():
    return _fetch_all("SELECT buyer_login, COUNT(*) AS total_bids, MAX(bid_amount) AS highest_bid FROM bid GROUP BY buyer_login ORDER BY buyer_login;")


def report_auctions_by_seller():
    return _fetch_all("SELECT seller_login, COUNT(*) AS total_auctions FROM auction GROUP BY seller_login ORDER BY seller_login;")


def report_payments_by_status():
    return _fetch_all("SELECT payment_status, COUNT(*) AS payment_count FROM payment GROUP BY payment_status ORDER BY payment_status;")
