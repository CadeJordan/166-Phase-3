import sys
import psycopg2
import psycopg2.extras


DB_CONFIG = {
    "dbname": None,
    "dbport": "5432",
    "user": None,
    "passwd": "",
}


def configure_db(dbname, dbport, user, passwd=""):
    """Set database connection info once before calling the query functions."""
    DB_CONFIG["dbname"] = dbname
    DB_CONFIG["dbport"] = str(dbport)
    DB_CONFIG["user"] = user
    DB_CONFIG["passwd"] = passwd


class EmbeddedSQL:
    """Small PostgreSQL helper class, same style as the previous lab file."""

    def __init__(self, dbname, dbport, user, passwd=""):
        try:
            self._connection = psycopg2.connect(
                database=dbname,
                user=user,
                password=passwd,
                host="localhost",
                port=dbport,
            )
        except Exception as e:
            print(f"Error - Unable to Connect to Database: {e}", file=sys.stderr)
            raise

    def execute_query(self, query, params=None):
        cursor = self._connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, params)
        rows = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        return rows

    def execute_one(self, query, params=None):
        cursor = self._connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, params)
        row = cursor.fetchone()
        cursor.close()
        return dict(row) if row else None

    def execute_update(self, sql, params=None):
        cursor = self._connection.cursor()
        cursor.execute(sql, params)
        affected = cursor.rowcount
        self._connection.commit()
        cursor.close()
        return affected

    def cleanup(self):
        try:
            if self._connection is not None:
                self._connection.close()
        except Exception:
            pass


def _connect():
    if not DB_CONFIG["dbname"] or not DB_CONFIG["user"]:
        raise RuntimeError("Database is not configured. Call configure_db(dbname, dbport, user, passwd='') first.")
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


def _next_id(table_name, id_column):
    row = _fetch_one(f"SELECT COALESCE(MAX({id_column}), 0) + 1 AS next_id FROM {table_name};")
    return row["next_id"]


# ----------------------------------------------------------
# Demo setup from adjusted queries.sql
# ----------------------------------------------------------

def setup_demo_data():
    """Insert a small safe demo dataset that satisfies all foreign keys."""
    esql = _connect()
    try:
        commands = [
            ("INSERT INTO users (login, password, phone_num, address, role, favorite_category) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (login) DO NOTHING;",
             ("admin1", "adminpass", "111-111-1111", "Admin Address", "Admin", None)),
            ("INSERT INTO users (login, password, phone_num, address, role, favorite_category) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (login) DO NOTHING;",
             ("seller1", "sellerpass", "222-222-2222", "Seller Address", "Seller", "Electronics")),
            ("INSERT INTO users (login, password, phone_num, address, role, favorite_category) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (login) DO NOTHING;",
             ("buyer1", "buyerpass", "333-333-3333", "Buyer Address", "Buyer", "Electronics")),
            ("INSERT INTO users (login, password, phone_num, address, role, favorite_category) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (login) DO NOTHING;",
             ("buyer2", "buyerpass", "444-444-4444", "Buyer 2 Address", "Buyer", "Books")),
            ("INSERT INTO item (item_id, item_name, category, starting_price, image_url, item_condition, description, seller_login, seller_role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (item_id) DO NOTHING;",
             (9001, "MacBook Pro", "Electronics", 700.00, None, "Used", "2021 MacBook Pro", "seller1", "Seller")),
            ("INSERT INTO auction (auction_id, item_id, seller_login, seller_role, current_highest_bid, auction_status, winner_login, winner_role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (auction_id) DO NOTHING;",
             (9001, 9001, "seller1", "Seller", 700.00, "Active", None, "Buyer")),
        ]
        for sql, params in commands:
            esql.execute_update(sql, params)
        return True
    finally:
        esql.cleanup()


def get_categories():
    return _fetch_all("SELECT DISTINCT category FROM item ORDER BY category;")


def get_all_users():
    return _fetch_all("SELECT login, phone_num, address, role, favorite_category FROM users ORDER BY login;")


def get_all_items():
    return _fetch_all("SELECT item_id, item_name, category, starting_price, image_url, item_condition, description, seller_login, seller_role FROM item ORDER BY item_id;")


def get_user(login):
    return _fetch_one("SELECT login, phone_num, address, role, favorite_category FROM users WHERE login = %s;", (login,))


def get_item(item_id):
    return _fetch_one("SELECT item_id, item_name, category, starting_price, image_url, item_condition, description, seller_login, seller_role FROM item WHERE item_id = %s;", (item_id,))


def get_auction_with_item(auction_id):
    return _fetch_one("SELECT a.auction_id, a.item_id, i.item_name, i.category, i.description, i.item_condition, i.starting_price, a.current_highest_bid, a.auction_status, a.seller_login, a.winner_login FROM auction a JOIN item i ON a.item_id = i.item_id WHERE a.auction_id = %s;", (auction_id,))


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

    return _fetch_all(sql, tuple(params))


def get_user_bids(login):
    return _fetch_all("SELECT b.bid_id, b.auction_id, b.bid_amount, b.bid_timestamp, i.item_name, i.category, a.auction_status, a.current_highest_bid FROM bid b JOIN auction a ON b.auction_id = a.auction_id JOIN item i ON a.item_id = i.item_id WHERE b.buyer_login = %s ORDER BY b.bid_timestamp DESC;", (login,))


def get_user_wins(login):
    return _fetch_all("SELECT a.auction_id, i.item_name, i.category, a.current_highest_bid, p.payment_status, s.shipment_status, s.tracking_number FROM auction a JOIN item i ON a.item_id = i.item_id LEFT JOIN payment p ON a.auction_id = p.auction_id LEFT JOIN shipment s ON a.auction_id = s.auction_id WHERE a.winner_login = %s AND a.auction_status = 'Closed' ORDER BY a.auction_id DESC;", (login,))


def get_seller_listings(login):
    return _fetch_all("SELECT i.item_id, i.item_name, i.category, i.starting_price, i.item_condition, i.description, a.auction_id, a.current_highest_bid, a.auction_status, COUNT(b.bid_id) AS bid_count FROM item i LEFT JOIN auction a ON i.item_id = a.item_id LEFT JOIN bid b ON a.auction_id = b.auction_id WHERE i.seller_login = %s GROUP BY i.item_id, i.item_name, i.category, i.starting_price, i.item_condition, i.description, a.auction_id, a.current_highest_bid, a.auction_status ORDER BY i.item_id DESC;", (login,))


def get_all_auctions_enriched():
    return _fetch_all("SELECT a.auction_id, i.item_name, i.category, a.seller_login, a.current_highest_bid, a.auction_status, a.winner_login, COUNT(b.bid_id) AS bid_count FROM auction a JOIN item i ON a.item_id = i.item_id LEFT JOIN bid b ON a.auction_id = b.auction_id GROUP BY a.auction_id, i.item_name, i.category, a.seller_login, a.current_highest_bid, a.auction_status, a.winner_login ORDER BY a.auction_id DESC;")


def get_payments(status_filter=""):
    if status_filter:
        return _fetch_all("SELECT p.payment_id, p.auction_id, p.buyer_login, p.amount, p.payment_status, i.item_name FROM payment p JOIN auction a ON p.auction_id = a.auction_id JOIN item i ON a.item_id = i.item_id WHERE p.payment_status = %s ORDER BY p.payment_id;", (status_filter,))
    return _fetch_all("SELECT p.payment_id, p.auction_id, p.buyer_login, p.amount, p.payment_status, i.item_name FROM payment p JOIN auction a ON p.auction_id = a.auction_id JOIN item i ON a.item_id = i.item_id ORDER BY p.payment_id;")


def get_shipments():
    return _fetch_all("SELECT s.shipment_id, s.auction_id, s.address, s.shipment_status, s.tracking_number, i.item_name FROM shipment s JOIN auction a ON s.auction_id = a.auction_id JOIN item i ON a.item_id = i.item_id ORDER BY s.shipment_id;")


def get_admin_stats():
    return _fetch_one("SELECT (SELECT COUNT(*) FROM users) AS total_users, (SELECT COUNT(*) FROM item) AS total_items, (SELECT COUNT(*) FROM auction WHERE auction_status = 'Active') AS active_auctions, (SELECT COUNT(*) FROM auction WHERE auction_status = 'Closed') AS closed_auctions, (SELECT COUNT(*) FROM bid) AS total_bids, (SELECT COUNT(*) FROM payment) AS total_payments, (SELECT COUNT(*) FROM shipment) AS total_shipments;")


def get_seller_hub_stats(login):
    stats = _fetch_one("SELECT COUNT(DISTINCT a.auction_id) FILTER (WHERE a.auction_status = 'Active') AS active_listings, COUNT(b.bid_id) AS total_bids FROM item i LEFT JOIN auction a ON i.item_id = a.item_id LEFT JOIN bid b ON a.auction_id = b.auction_id WHERE i.seller_login = %s;", (login,))
    listings = get_seller_listings(login)
    if stats is None:
        stats = {"active_listings": 0, "total_bids": 0}
    stats["listings"] = listings
    return stats


def authenticate_user(login, password):
    return _fetch_one("SELECT login, phone_num, address, role, favorite_category FROM users WHERE login = %s AND password = %s;", (login, password))


def register_user(phone_num, login, password, address, favorite_category=None):
    return _execute("INSERT INTO users (login, password, phone_num, address, role, favorite_category) VALUES (%s, %s, %s, %s, 'Buyer', %s);", (login, password, phone_num, address, favorite_category))


def update_user_profile(login, phone_num, address, favorite_category=None):
    return _execute("UPDATE users SET phone_num = %s, address = %s, favorite_category = %s WHERE login = %s;", (phone_num, address, favorite_category, login))


def place_bid(auction_id, buyer_login, bid_amount):
    """Insert bid and update current_highest_bid only if the bid is valid."""
    esql = _connect()
    try:
        cursor = esql._connection.cursor()
        cursor.execute("SELECT COALESCE(MAX(bid_id), 0) + 1 FROM bid;")
        bid_id = cursor.fetchone()[0]
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
    """Create an item and its active auction. Returns created IDs."""
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
    return _execute("UPDATE auction SET auction_status = 'Closed', winner_login = (SELECT buyer_login FROM bid WHERE auction_id = %s ORDER BY bid_amount DESC, bid_timestamp ASC LIMIT 1), winner_role = 'Buyer' WHERE auction_id = %s AND seller_login = %s AND auction_status = 'Active';", (auction_id, auction_id, seller_login))


def update_user_role(login, new_role):
    return _execute("UPDATE users SET role = %s WHERE login = %s;", (new_role, login))


def remove_item(item_id):
    """Delete an item only if no auction depends on it, because schema uses ON DELETE RESTRICT."""
    return _execute("DELETE FROM item WHERE item_id = %s;", (item_id,))


def process_payment(auction_id, buyer_login):
    """Create a payment for a closed auction won by buyer_login, or mark existing payment Completed."""
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


# import sys
# from EmbeddedSQL import EmbeddedSQL
# from data import mock_data

# _esql = None


# def configure_db(dbname, dbport, user, passwd=""):
#     """Create one shared EmbeddedSQL connection for all query functions."""
#     global _esql
#     if _esql is not None:
#         _esql.cleanup()
#     _esql = EmbeddedSQL(dbname, dbport, user, passwd)
#     return _esql


# def set_esql(esql):
#     """Let another file pass in an already-created EmbeddedSQL object."""
#     global _esql
#     _esql = esql


# def cleanup():
#     """Close the shared database connection."""
#     global _esql
#     if _esql is not None:
#         _esql.cleanup()
#         _esql = None


# def _conn():
#     if _esql is None:
#         raise RuntimeError("Database is not configured. Call configure_db(dbname, dbport, user) first.")
#     return _esql._connection


# def _fetch_all(query, params=None):
#     cursor = _conn().cursor()
#     cursor.execute(query, params or ())
#     columns = [desc[0] for desc in cursor.description]
#     rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
#     cursor.close()
#     return rows


# def _fetch_one(query, params=None):
#     rows = _fetch_all(query, params)
#     return rows[0] if rows else None


# def _execute(query, params=None):
#     cursor = _conn().cursor()
#     try:
#         cursor.execute(query, params or ())
#         affected = cursor.rowcount
#         _conn().commit()
#         return affected
#     except Exception:
#         _conn().rollback()
#         raise
#     finally:
#         cursor.close()


# def _next_id(table_name, column_name):
#     # table/column names are constants passed by this file only, not user input.
#     row = _fetch_one(f"SELECT COALESCE(MAX({column_name}), 0) + 1 AS next_id FROM {table_name};")
#     return row["next_id"]

#     cursor = _conn().cursor()
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


# def get_categories():
#     """SQL: SELECT DISTINCT category FROM item ORDER BY category."""
#     rows = _fetch_all("SELECT DISTINCT category FROM item ORDER BY category;")
#     return [row["category"] for row in rows]


# def get_all_users():
#     """SQL: SELECT login, phone_num, address, role, favorite_category FROM users."""
#     return _fetch_all("SELECT login, phone_num, address, role, favorite_category FROM users ORDER BY login;")


# def get_all_items():
#     """SQL: SELECT * FROM item."""
#     return _fetch_all("SELECT item_id, item_name, category, starting_price, image_url, item_condition, description, seller_login, seller_role FROM item ORDER BY item_id;")


# def get_user(login):
#     """SQL: SELECT * FROM users WHERE login = %s."""
#     return _fetch_one("SELECT login, password, phone_num, address, role, favorite_category FROM users WHERE login = %s;", (login,))


# def get_item(item_id):
#     """SQL: SELECT * FROM item WHERE item_id = %s."""
#     return _fetch_one("SELECT item_id, item_name, category, starting_price, image_url, item_condition, description, seller_login, seller_role FROM item WHERE item_id = %s;", (item_id,))


# def get_auction_with_item(auction_id):
#     """SQL: JOIN auction + item for a single auction_id."""
#     return _fetch_one(
#         "SELECT a.auction_id, a.item_id, a.seller_login, a.seller_role, a.current_highest_bid, a.auction_status, a.winner_login, a.winner_role, i.item_name, i.category, i.starting_price, i.image_url, i.item_condition, i.description FROM auction a JOIN item i ON a.item_id = i.item_id WHERE a.auction_id = %s;",
#         (auction_id,)
#     )


# def get_bids_for_auction(auction_id):
#     """SQL: SELECT * FROM bid WHERE auction_id = %s ORDER BY bid_timestamp DESC."""
#     return _fetch_all("SELECT bid_id, auction_id, buyer_login, buyer_role, bid_amount, bid_timestamp FROM bid WHERE auction_id = %s ORDER BY bid_timestamp DESC;", (auction_id,))


# def get_payment_for_auction(auction_id):
#     """SQL: SELECT * FROM payment WHERE auction_id = %s."""
#     return _fetch_one("SELECT payment_id, auction_id, buyer_login, buyer_role, amount, payment_status FROM payment WHERE auction_id = %s;", (auction_id,))


# def get_shipment_for_auction(auction_id):
#     """SQL: SELECT * FROM shipment WHERE auction_id = %s."""
#     return _fetch_one("SELECT shipment_id, auction_id, address, shipment_status, tracking_number FROM shipment WHERE auction_id = %s;", (auction_id,))


# def search_auctions(q="", category="", status="", sort="newest"):
#     """
#     SQL: JOIN auction + item with optional filters.
#     sort: newest | price_asc | price_desc
#     """
#     where = []
#     params = []

#     if q:
#         where.append("LOWER(i.item_name) LIKE LOWER(%s)")
#         params.append(f"%{q}%")
#     if category:
#         where.append("i.category = %s")
#         params.append(category)
#     if status:
#         where.append("a.auction_status = %s")
#         params.append(status)

#     order_by = "a.auction_id DESC"
#     if sort == "price_asc":
#         order_by = "a.current_highest_bid ASC"
#     elif sort == "price_desc":
#         order_by = "a.current_highest_bid DESC"

#     sql = "SELECT a.auction_id, a.item_id, a.seller_login, a.current_highest_bid, a.auction_status, a.winner_login, i.item_name, i.category, i.description, i.item_condition, i.starting_price, i.image_url FROM auction a JOIN item i ON a.item_id = i.item_id"
#     if where:
#         sql += " WHERE " + " AND ".join(where)
#     sql += f" ORDER BY {order_by};"

#     return _fetch_all(sql, tuple(params))


# def get_user_bids(login):
#     """SQL: bids by buyer joined with auction + item."""
#     return _fetch_all(
#         "SELECT b.bid_id, b.auction_id, b.buyer_login, b.bid_amount, b.bid_timestamp, a.auction_status, a.current_highest_bid, i.item_name, i.category FROM bid b JOIN auction a ON b.auction_id = a.auction_id JOIN item i ON a.item_id = i.item_id WHERE b.buyer_login = %s ORDER BY b.bid_timestamp DESC;",
#         (login,)
#     )


# def get_user_wins(login):
#     """SQL: closed auctions where winner_login = login, plus payment/shipment."""
#     return _fetch_all(
#         "SELECT a.auction_id, a.current_highest_bid, a.auction_status, a.winner_login, i.item_name, i.category, p.payment_id, p.payment_status, s.shipment_id, s.shipment_status, s.tracking_number FROM auction a JOIN item i ON a.item_id = i.item_id LEFT JOIN payment p ON a.auction_id = p.auction_id LEFT JOIN shipment s ON a.auction_id = s.auction_id WHERE a.auction_status = 'Closed' AND a.winner_login = %s ORDER BY a.auction_id DESC;",
#         (login,)
#     )


# def get_seller_listings(login):
#     """SQL: items by seller joined with auction and bid count."""
#     return _fetch_all(
#         "SELECT i.item_id, i.item_name, i.category, i.starting_price, i.image_url, i.item_condition, i.description, a.auction_id, a.current_highest_bid, a.auction_status, a.winner_login, COUNT(b.bid_id) AS bid_count FROM item i LEFT JOIN auction a ON i.item_id = a.item_id LEFT JOIN bid b ON a.auction_id = b.auction_id WHERE i.seller_login = %s GROUP BY i.item_id, i.item_name, i.category, i.starting_price, i.image_url, i.item_condition, i.description, a.auction_id, a.current_highest_bid, a.auction_status, a.winner_login ORDER BY i.item_id DESC;",
#         (login,)
#     )


# def get_all_auctions_enriched():
#     """SQL: all auctions joined with item and bid count."""
#     return _fetch_all(
#         "SELECT a.auction_id, a.item_id, a.seller_login, a.current_highest_bid, a.auction_status, a.winner_login, i.item_name, i.category, i.description, i.item_condition, COUNT(b.bid_id) AS bid_count FROM auction a JOIN item i ON a.item_id = i.item_id LEFT JOIN bid b ON a.auction_id = b.auction_id GROUP BY a.auction_id, a.item_id, a.seller_login, a.current_highest_bid, a.auction_status, a.winner_login, i.item_name, i.category, i.description, i.item_condition ORDER BY a.auction_id DESC;"
#     )


# # def get_payments(status_filter=""):
# #     """SQL: payments joined with auction/item, optional status filter."""
# #     payments = mock_data.PAYMENTS
# #     if status_filter:
# #         payments = [p for p in payments if p["payment_status"] == status_filter]
# #     enriched = []
# #     for p in payments:
# #         auction = mock_data.get_auction_with_item(p["auction_id"])
# #         enriched.append({**p, "auction": auction})
# #     return enriched
# def get_payments(status_filter=""):
#     """SQL: payments joined with auction/item, optional status filter."""
#     if status_filter:
#         return _fetch_all(
#             "SELECT p.payment_id, p.auction_id, p.buyer_login, p.amount, p.payment_status, i.item_name, i.category FROM payment p JOIN auction a ON p.auction_id = a.auction_id JOIN item i ON a.item_id = i.item_id WHERE p.payment_status = %s ORDER BY p.payment_id;",
#             (status_filter,)
#         )
#     return _fetch_all(
#         "SELECT p.payment_id, p.auction_id, p.buyer_login, p.amount, p.payment_status, i.item_name, i.category FROM payment p JOIN auction a ON p.auction_id = a.auction_id JOIN item i ON a.item_id = i.item_id ORDER BY p.payment_id;"
#     )


# # def get_shipments():
# #     """SQL: shipments joined with auction/item."""
# #     enriched = []
# #     for s in mock_data.SHIPMENTS:
# #         auction = mock_data.get_auction_with_item(s["auction_id"])
# #         enriched.append({**s, "auction": auction})
# #     return enriched

# def get_shipments():
#     """SQL: shipments joined with auction/item."""
#     return _fetch_all(
#         "SELECT s.shipment_id, s.auction_id, s.address, s.shipment_status, s.tracking_number, i.item_name, i.category FROM shipment s JOIN auction a ON s.auction_id = a.auction_id JOIN item i ON a.item_id = i.item_id ORDER BY s.shipment_id;"
#     )


# # def get_admin_stats():
# #     """SQL: aggregate counts for dashboard cards."""
# #     return mock_data.get_admin_stats()


# def get_admin_stats():
#     """SQL: aggregate counts for dashboard cards."""
#     return {
#         "users": _fetch_one("SELECT COUNT(*) AS count FROM users;")["count"],
#         "items": _fetch_one("SELECT COUNT(*) AS count FROM item;")["count"],
#         "auctions": _fetch_one("SELECT COUNT(*) AS count FROM auction;")["count"],
#         "active_auctions": _fetch_one("SELECT COUNT(*) AS count FROM auction WHERE auction_status = 'Active';")["count"],
#         "closed_auctions": _fetch_one("SELECT COUNT(*) AS count FROM auction WHERE auction_status = 'Closed';")["count"],
#         "bids": _fetch_one("SELECT COUNT(*) AS count FROM bid;")["count"],
#         "payments": _fetch_one("SELECT COUNT(*) AS count FROM payment;")["count"],
#         "shipments": _fetch_one("SELECT COUNT(*) AS count FROM shipment;")["count"],
#     }


# # def get_seller_hub_stats(login):
# #     """SQL: active listing count and total bids for seller."""
# #     listings = mock_data.get_seller_listings(login)
# #     active = len([l for l in listings if l["auction"] and l["auction"]["auction_status"] == "Active"])
# #     total_bids = sum(l["bid_count"] for l in listings)
# #     return {"active_listings": active, "total_bids": total_bids, "listings": listings}

# def get_seller_hub_stats(login):
#     """SQL: active listing count and total bids for seller."""
#     stats = _fetch_one(
#         "SELECT COUNT(DISTINCT a.auction_id) FILTER (WHERE a.auction_status = 'Active') AS active_listings, COUNT(b.bid_id) AS total_bids FROM auction a LEFT JOIN bid b ON a.auction_id = b.auction_id WHERE a.seller_login = %s;",
#         (login,)
#     )
#     listings = get_seller_listings(login)
#     return {
#         "active_listings": stats["active_listings"] if stats else 0,
#         "total_bids": stats["total_bids"] if stats else 0,
#         "listings": listings,
#     }


# def authenticate_user(login, password):
#     """SQL: verify login/password. Return user dict or None."""
#     return _fetch_one("SELECT login, phone_num, address, role, favorite_category FROM users WHERE login = %s AND password = %s;", (login, password))


# def register_user(phone_num, login, password, address, favorite_category=None):
#     """SQL: INSERT INTO users. New accounts default to Buyer."""
#     _execute(
#         "INSERT INTO users (login, password, phone_num, address, role, favorite_category) VALUES (%s, %s, %s, %s, 'Buyer', %s);",
#         (login, password, phone_num, address, favorite_category)
#     )
#     return get_user(login)


# def update_user_profile(login, phone_num, address, favorite_category=None):
#     """SQL: UPDATE users SET phone_num, address, favorite_category WHERE login = %s."""
#     _execute(
#         "UPDATE users SET phone_num = %s, address = %s, favorite_category = %s WHERE login = %s;",
#         (phone_num, address, favorite_category, login)
#     )
#     return get_user(login)


# def place_bid(auction_id, buyer_login, bid_amount):
#     """SQL: INSERT bid + UPDATE auction.current_highest_bid with constraints."""
#     bid_id = _next_id("bid", "bid_id")
#     cursor = _conn().cursor()
#     try:
#         cursor.execute(
#             "INSERT INTO bid (bid_id, auction_id, buyer_login, buyer_role, bid_amount) SELECT %s, auction_id, %s, 'Buyer', %s FROM auction WHERE auction_id = %s AND auction_status = 'Active' AND seller_login <> %s AND %s > current_highest_bid;",
#             (bid_id, buyer_login, bid_amount, auction_id, buyer_login, bid_amount)
#         )
#         inserted = cursor.rowcount
#         if inserted == 0:
#             _conn().rollback()
#             cursor.close()
#             return {"success": False, "message": "Bid rejected. Auction must be active, bid must be higher, and seller cannot bid on own auction."}

#         cursor.execute(
#             "UPDATE auction SET current_highest_bid = %s WHERE auction_id = %s;",
#             (bid_amount, auction_id)
#         )
#         _conn().commit()
#         cursor.close()
#         return {"success": True, "bid_id": bid_id, "auction_id": auction_id, "bid_amount": bid_amount}
#     except Exception as e:
#         _conn().rollback()
#         cursor.close()
#         raise e


# def create_listing(seller_login, item_name, category, starting_price, **kwargs):
#     """SQL: INSERT item + INSERT auction with status Active."""
#     item_id = kwargs.get("item_id") or _next_id("item", "item_id")
#     auction_id = kwargs.get("auction_id") or _next_id("auction", "auction_id")
#     image_url = kwargs.get("image_url")
#     item_condition = kwargs.get("item_condition") or kwargs.get("condition")
#     description = kwargs.get("description")

#     cursor = _conn().cursor()
#     try:
#         cursor.execute(
#             "INSERT INTO item (item_id, item_name, category, starting_price, image_url, item_condition, description, seller_login, seller_role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Seller');",
#             (item_id, item_name, category, starting_price, image_url, item_condition, description, seller_login)
#         )
#         cursor.execute(
#             "INSERT INTO auction (auction_id, item_id, seller_login, seller_role, current_highest_bid, auction_status, winner_login, winner_role) VALUES (%s, %s, %s, 'Seller', %s, 'Active', NULL, 'Buyer');",
#             (auction_id, item_id, seller_login, starting_price)
#         )
#         _conn().commit()
#         cursor.close()
#         return get_auction_with_item(auction_id)
#     except Exception as e:
#         _conn().rollback()
#         cursor.close()
#         raise e


# def update_listing(item_id, seller_login, **fields):
#     """SQL: UPDATE item WHERE item_id AND seller_login match."""
#     allowed = {
#         "item_name": "item_name",
#         "category": "category",
#         "starting_price": "starting_price",
#         "image_url": "image_url",
#         "item_condition": "item_condition",
#         "condition": "item_condition",
#         "description": "description",
#     }

#     assignments = []
#     params = []
#     for key, value in fields.items():
#         if key in allowed:
#             assignments.append(f"{allowed[key]} = %s")
#             params.append(value)

#     if not assignments:
#         return get_item(item_id)

#     params.extend([item_id, seller_login])
#     _execute(
#         f"UPDATE item SET {', '.join(assignments)} WHERE item_id = %s AND seller_login = %s;",
#         tuple(params)
#     )
#     return get_item(item_id)


# def end_auction(auction_id, seller_login):
#     """SQL: set auction_status Closed, set winner_login to highest bidder."""
#     _execute(
#         "UPDATE auction SET auction_status = 'Closed', winner_login = (SELECT buyer_login FROM bid WHERE auction_id = %s ORDER BY bid_amount DESC, bid_timestamp ASC LIMIT 1), winner_role = 'Buyer' WHERE auction_id = %s AND seller_login = %s AND auction_status = 'Active';",
#         (auction_id, auction_id, seller_login)
#     )
#     return get_auction_with_item(auction_id)


# def update_user_role(login, new_role):
#     """SQL: UPDATE users SET role — admin only in app/front-end logic."""
#     _execute("UPDATE users SET role = %s WHERE login = %s;", (new_role, login))
#     return get_user(login)


# def remove_item(item_id):
#     """SQL: DELETE item. FK constraints may prevent deleting active/referenced items."""
#     return _execute("DELETE FROM item WHERE item_id = %s;", (item_id,))


# def process_payment(auction_id, buyer_login):
#     """SQL: INSERT payment for a closed won auction or mark existing payment completed."""
#     existing = get_payment_for_auction(auction_id)
#     if existing:
#         _execute(
#             "UPDATE payment SET payment_status = 'Completed' WHERE auction_id = %s AND buyer_login = %s;",
#             (auction_id, buyer_login)
#         )
#         return get_payment_for_auction(auction_id)

#     payment_id = _next_id("payment", "payment_id")
#     _execute(
#         "INSERT INTO payment (payment_id, auction_id, buyer_login, buyer_role, amount, payment_status) SELECT %s, auction_id, winner_login, 'Buyer', current_highest_bid, 'Completed' FROM auction WHERE auction_id = %s AND auction_status = 'Closed' AND winner_login = %s;",
#         (payment_id, auction_id, buyer_login)
#     )
#     return get_payment_for_auction(auction_id)


# def update_shipment(shipment_id, shipment_status, tracking_number=None):
#     """SQL: UPDATE shipment."""
#     _execute(
#         "UPDATE shipment SET shipment_status = %s, tracking_number = %s WHERE shipment_id = %s;",
#         (shipment_status, tracking_number, shipment_id)
#     )
#     return _fetch_one("SELECT shipment_id, auction_id, address, shipment_status, tracking_number FROM shipment WHERE shipment_id = %s;", (shipment_id,))