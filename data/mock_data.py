"""AI generated mock data"""

from datetime import datetime

CATEGORIES = [
    "Electronics",
    "Collectibles",
    "Fashion",
    "Home & Garden",
    "Sports",
    "Toys",
]

USERS = [
    {
        "login": "buyer1",
        "password": "buyer123",
        "phone_num": "555-0101",
        "address": "123 Main St, Austin, TX 78701",
        "role": "Buyer",
        "favorite_category": "Electronics",
    },
    {
        "login": "buyer2",
        "password": "buyer456",
        "phone_num": "555-0102",
        "address": "456 Oak Ave, Dallas, TX 75201",
        "role": "Buyer",
        "favorite_category": "Collectibles",
    },
    {
        "login": "seller1",
        "password": "seller123",
        "phone_num": "555-0201",
        "address": "789 Pine Rd, Houston, TX 77001",
        "role": "Seller",
        "favorite_category": "Electronics",
    },
    {
        "login": "seller2",
        "password": "seller456",
        "phone_num": "555-0202",
        "address": "321 Elm Blvd, San Antonio, TX 78201",
        "role": "Seller",
        "favorite_category": "Fashion",
    },
    {
        "login": "admin1",
        "password": "admin123",
        "phone_num": "555-0301",
        "address": "100 Admin Way, Austin, TX 78702",
        "role": "Admin",
        "favorite_category": None,
    },
]

ITEMS = [
    {
        "item_id": 1,
        "item_name": "Vintage Canon AE-1 Camera",
        "category": "Electronics",
        "starting_price": 75.00,
        "image_url": "https://placehold.co/400x400/e8e8e8/666?text=Camera",
        "item_condition": "Used - Good",
        "description": "Classic 35mm film camera in working condition. Includes original lens cap.",
        "seller_login": "seller1",
        "seller_role": "Seller",
    },
    {
        "item_id": 2,
        "item_name": "Nintendo Switch OLED Console",
        "category": "Electronics",
        "starting_price": 200.00,
        "image_url": "https://placehold.co/400x400/e8e8e8/666?text=Switch",
        "item_condition": "Used - Like New",
        "description": "White OLED model with dock and two Joy-Con controllers.",
        "seller_login": "seller1",
        "seller_role": "Seller",
    },
    {
        "item_id": 3,
        "item_name": "1952 Mickey Mantle Rookie Card (Reprint)",
        "category": "Collectibles",
        "starting_price": 25.00,
        "image_url": "https://placehold.co/400x400/e8e8e8/666?text=Card",
        "item_condition": "New",
        "description": "High-quality reprint in protective sleeve.",
        "seller_login": "seller2",
        "seller_role": "Seller",
    },
    {
        "item_id": 4,
        "item_name": "Levi's 501 Original Jeans",
        "category": "Fashion",
        "starting_price": 30.00,
        "image_url": "https://placehold.co/400x400/e8e8e8/666?text=Jeans",
        "item_condition": "Used - Good",
        "description": "Size 32x32, dark wash, minimal wear.",
        "seller_login": "seller2",
        "seller_role": "Seller",
    },
    {
        "item_id": 5,
        "item_name": "Weber Spirit II E-310 Grill",
        "category": "Home & Garden",
        "starting_price": 150.00,
        "image_url": "https://placehold.co/400x400/e8e8e8/666?text=Grill",
        "item_condition": "Used - Good",
        "description": "3-burner gas grill with cover. Pickup only.",
        "seller_login": "seller1",
        "seller_role": "Seller",
    },
    {
        "item_id": 6,
        "item_name": "Wilson Pro Staff Tennis Racket",
        "category": "Sports",
        "starting_price": 45.00,
        "image_url": "https://placehold.co/400x400/e8e8e8/666?text=Racket",
        "item_condition": "Used - Like New",
        "description": "Grip size 4 3/8, freshly restrung.",
        "seller_login": "seller2",
        "seller_role": "Seller",
    },
    {
        "item_id": 7,
        "item_name": "LEGO Star Wars Millennium Falcon",
        "category": "Toys",
        "starting_price": 80.00,
        "image_url": "https://placehold.co/400x400/e8e8e8/666?text=LEGO",
        "item_condition": "Used - Good",
        "description": "Complete set with box and instructions.",
        "seller_login": "seller1",
        "seller_role": "Seller",
    },
    {
        "item_id": 8,
        "item_name": "Sony WH-1000XM4 Headphones",
        "category": "Electronics",
        "starting_price": 120.00,
        "image_url": "https://placehold.co/400x400/e8e8e8/666?text=Headphones",
        "item_condition": "Used - Like New",
        "description": "Black, noise-cancelling, includes carrying case.",
        "seller_login": "seller1",
        "seller_role": "Seller",
    },
]

AUCTIONS = [
    {
        "auction_id": 1,
        "item_id": 1,
        "seller_login": "seller1",
        "seller_role": "Seller",
        "current_highest_bid": 95.00,
        "auction_status": "Active",
        "winner_login": None,
        "winner_role": None,
    },
    {
        "auction_id": 2,
        "item_id": 2,
        "seller_login": "seller1",
        "seller_role": "Seller",
        "current_highest_bid": 245.00,
        "auction_status": "Active",
        "winner_login": None,
        "winner_role": None,
    },
    {
        "auction_id": 3,
        "item_id": 3,
        "seller_login": "seller2",
        "seller_role": "Seller",
        "current_highest_bid": 38.50,
        "auction_status": "Active",
        "winner_login": None,
        "winner_role": None,
    },
    {
        "auction_id": 4,
        "item_id": 4,
        "seller_login": "seller2",
        "seller_role": "Seller",
        "current_highest_bid": 42.00,
        "auction_status": "Active",
        "winner_login": None,
        "winner_role": None,
    },
    {
        "auction_id": 5,
        "item_id": 5,
        "seller_login": "seller1",
        "seller_role": "Seller",
        "current_highest_bid": 175.00,
        "auction_status": "Active",
        "winner_login": None,
        "winner_role": None,
    },
    {
        "auction_id": 6,
        "item_id": 6,
        "seller_login": "seller2",
        "seller_role": "Seller",
        "current_highest_bid": 55.00,
        "auction_status": "Closed",
        "winner_login": "buyer1",
        "winner_role": "Buyer",
    },
    {
        "auction_id": 7,
        "item_id": 7,
        "seller_login": "seller1",
        "seller_role": "Seller",
        "current_highest_bid": 110.00,
        "auction_status": "Closed",
        "winner_login": "buyer2",
        "winner_role": "Buyer",
    },
    {
        "auction_id": 8,
        "item_id": 8,
        "seller_login": "seller1",
        "seller_role": "Seller",
        "current_highest_bid": 145.00,
        "auction_status": "Active",
        "winner_login": None,
        "winner_role": None,
    },
]

BIDS = [
    {"bid_id": 1, "auction_id": 1, "buyer_login": "buyer1", "buyer_role": "Buyer", "bid_amount": 80.00, "bid_timestamp": datetime(2026, 5, 28, 10, 15)},
    {"bid_id": 2, "auction_id": 1, "buyer_login": "buyer2", "buyer_role": "Buyer", "bid_amount": 85.00, "bid_timestamp": datetime(2026, 5, 28, 14, 30)},
    {"bid_id": 3, "auction_id": 1, "buyer_login": "buyer1", "buyer_role": "Buyer", "bid_amount": 95.00, "bid_timestamp": datetime(2026, 5, 29, 9, 0)},
    {"bid_id": 4, "auction_id": 2, "buyer_login": "buyer1", "buyer_role": "Buyer", "bid_amount": 210.00, "bid_timestamp": datetime(2026, 5, 27, 11, 0)},
    {"bid_id": 5, "auction_id": 2, "buyer_login": "buyer2", "buyer_role": "Buyer", "bid_amount": 225.00, "bid_timestamp": datetime(2026, 5, 28, 16, 45)},
    {"bid_id": 6, "auction_id": 2, "buyer_login": "buyer1", "buyer_role": "Buyer", "bid_amount": 245.00, "bid_timestamp": datetime(2026, 5, 30, 8, 20)},
    {"bid_id": 7, "auction_id": 3, "buyer_login": "buyer2", "buyer_role": "Buyer", "bid_amount": 30.00, "bid_timestamp": datetime(2026, 5, 29, 12, 0)},
    {"bid_id": 8, "auction_id": 3, "buyer_login": "buyer1", "buyer_role": "Buyer", "bid_amount": 35.00, "bid_timestamp": datetime(2026, 5, 30, 10, 30)},
    {"bid_id": 9, "auction_id": 3, "buyer_login": "buyer2", "buyer_role": "Buyer", "bid_amount": 38.50, "bid_timestamp": datetime(2026, 6, 1, 15, 0)},
    {"bid_id": 10, "auction_id": 4, "buyer_login": "buyer1", "buyer_role": "Buyer", "bid_amount": 35.00, "bid_timestamp": datetime(2026, 5, 30, 9, 15)},
    {"bid_id": 11, "auction_id": 4, "buyer_login": "buyer2", "buyer_role": "Buyer", "bid_amount": 42.00, "bid_timestamp": datetime(2026, 6, 2, 11, 0)},
    {"bid_id": 12, "auction_id": 5, "buyer_login": "buyer2", "buyer_role": "Buyer", "bid_amount": 160.00, "bid_timestamp": datetime(2026, 6, 1, 13, 0)},
    {"bid_id": 13, "auction_id": 5, "buyer_login": "buyer1", "buyer_role": "Buyer", "bid_amount": 175.00, "bid_timestamp": datetime(2026, 6, 3, 10, 0)},
    {"bid_id": 14, "auction_id": 6, "buyer_login": "buyer1", "buyer_role": "Buyer", "bid_amount": 50.00, "bid_timestamp": datetime(2026, 5, 20, 10, 0)},
    {"bid_id": 15, "auction_id": 6, "buyer_login": "buyer2", "buyer_role": "Buyer", "bid_amount": 55.00, "bid_timestamp": datetime(2026, 5, 22, 14, 0)},
    {"bid_id": 16, "auction_id": 7, "buyer_login": "buyer2", "buyer_role": "Buyer", "bid_amount": 100.00, "bid_timestamp": datetime(2026, 5, 18, 9, 0)},
    {"bid_id": 17, "auction_id": 7, "buyer_login": "buyer1", "buyer_role": "Buyer", "bid_amount": 105.00, "bid_timestamp": datetime(2026, 5, 19, 11, 0)},
    {"bid_id": 18, "auction_id": 7, "buyer_login": "buyer2", "buyer_role": "Buyer", "bid_amount": 110.00, "bid_timestamp": datetime(2026, 5, 21, 16, 0)},
    {"bid_id": 19, "auction_id": 8, "buyer_login": "buyer1", "buyer_role": "Buyer", "bid_amount": 130.00, "bid_timestamp": datetime(2026, 6, 2, 8, 0)},
    {"bid_id": 20, "auction_id": 8, "buyer_login": "buyer2", "buyer_role": "Buyer", "bid_amount": 145.00, "bid_timestamp": datetime(2026, 6, 4, 12, 30)},
]

PAYMENTS = [
    {
        "payment_id": 1,
        "auction_id": 6,
        "buyer_login": "buyer1",
        "buyer_role": "Buyer",
        "amount": 55.00,
        "payment_status": "Completed",
    },
    {
        "payment_id": 2,
        "auction_id": 7,
        "buyer_login": "buyer2",
        "buyer_role": "Buyer",
        "amount": 110.00,
        "payment_status": "Pending",
    },
]

SHIPMENTS = [
    {
        "shipment_id": 1,
        "auction_id": 6,
        "address": "123 Main St, Austin, TX 78701",
        "shipment_status": "Delivered",
        "tracking_number": "1Z999AA10123456784",
    },
    {
        "shipment_id": 2,
        "auction_id": 7,
        "address": "456 Oak Ave, Dallas, TX 75201",
        "shipment_status": "Pending",
        "tracking_number": None,
    },
]


def get_user(login):
    return next((u for u in USERS if u["login"] == login), None)


def get_item(item_id):
    return next((i for i in ITEMS if i["item_id"] == item_id), None)


def get_auction(auction_id):
    return next((a for a in AUCTIONS if a["auction_id"] == auction_id), None)


def get_auction_with_item(auction_id):
    auction = get_auction(auction_id)
    if not auction:
        return None
    item = get_item(auction["item_id"])
    if not item:
        return None
    return {**auction, "item": item}


def enrich_auction(auction):
    item = get_item(auction["item_id"])
    bid_count = len([b for b in BIDS if b["auction_id"] == auction["auction_id"]])
    return {**auction, "item": item, "bid_count": bid_count}


def get_all_auctions_enriched():
    return [enrich_auction(a) for a in AUCTIONS]


def search_auctions(q="", category="", status="", sort="newest"):
    results = get_all_auctions_enriched()
    if q:
        q_lower = q.lower()
        results = [
            a for a in results
            if q_lower in a["item"]["item_name"].lower()
            or q_lower in (a["item"].get("description") or "").lower()
        ]
    if category:
        results = [a for a in results if a["item"]["category"] == category]
    if status:
        results = [a for a in results if a["auction_status"] == status]
    if sort == "price_asc":
        results.sort(key=lambda a: a["current_highest_bid"])
    elif sort == "price_desc":
        results.sort(key=lambda a: a["current_highest_bid"], reverse=True)
    else:
        results.sort(key=lambda a: a["auction_id"], reverse=True)
    return results


def get_bids_for_auction(auction_id):
    bids = [b for b in BIDS if b["auction_id"] == auction_id]
    return sorted(bids, key=lambda b: b["bid_timestamp"], reverse=True)


def get_user_bids(login):
    bids = [b for b in BIDS if b["buyer_login"] == login]
    enriched = []
    for bid in sorted(bids, key=lambda b: b["bid_timestamp"], reverse=True):
        auction = get_auction_with_item(bid["auction_id"])
        if auction:
            enriched.append({**bid, "auction": auction})
    return enriched


def get_user_wins(login):
    wins = []
    for auction in AUCTIONS:
        if auction["winner_login"] == login and auction["auction_status"] == "Closed":
            data = enrich_auction(auction)
            payment = next((p for p in PAYMENTS if p["auction_id"] == auction["auction_id"]), None)
            shipment = next((s for s in SHIPMENTS if s["auction_id"] == auction["auction_id"]), None)
            wins.append({**data, "payment": payment, "shipment": shipment})
    return wins


def get_seller_listings(login):
    items = [i for i in ITEMS if i["seller_login"] == login]
    enriched = []
    for item in items:
        auction = next((a for a in AUCTIONS if a["item_id"] == item["item_id"]), None)
        bid_count = len([b for b in BIDS if auction and b["auction_id"] == auction["auction_id"]])
        enriched.append({"item": item, "auction": auction, "bid_count": bid_count})
    return enriched


def get_payment_for_auction(auction_id):
    return next((p for p in PAYMENTS if p["auction_id"] == auction_id), None)


def get_shipment_for_auction(auction_id):
    return next((s for s in SHIPMENTS if s["auction_id"] == auction_id), None)


def get_admin_stats():
    active = len([a for a in AUCTIONS if a["auction_status"] == "Active"])
    pending_payments = len([p for p in PAYMENTS if p["payment_status"] == "Pending"])
    pending_shipments = len([s for s in SHIPMENTS if s["shipment_status"] == "Pending"])
    return {
        "total_users": len(USERS),
        "active_auctions": active,
        "pending_payments": pending_payments,
        "pending_shipments": pending_shipments,
    }
