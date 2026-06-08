from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort

from data import queries

seller_bp = Blueprint("seller", __name__)


def _current_seller():
    login = session.get("demo_user", "seller1")
    user = queries.get_user(login)
    if user and user["role"] == "Seller":
        return user
    return queries.get_user("seller1")


@seller_bp.route("/sell")
def hub():
    seller = _current_seller()
    stats = queries.get_seller_hub_stats(seller["login"])
    return render_template(
        "pages/seller/hub.html",
        seller=seller,
        active_listings=stats["active_listings"],
        total_bids=stats["total_bids"],
        listings=stats["listings"],
    )


@seller_bp.route("/sell/listings")
def listings():
    seller = _current_seller()
    listings_data = queries.get_seller_listings(seller["login"])
    return render_template("pages/seller/listings.html", listings=listings_data, seller=seller)


@seller_bp.route("/sell/create", methods=["GET", "POST"])
def create_listing():
    seller = _current_seller()
    if request.method == "POST":
        item_name = request.form.get("item_name", "").strip()
        category = request.form.get("category", "").strip()
        starting_price = request.form.get("starting_price", type=float)
        item_condition = request.form.get("item_condition") or None
        description = request.form.get("description") or None

        if not item_name or not category or starting_price is None:
            flash("Item name, category, and starting price are required.", "error")
            return redirect(url_for("seller.create_listing"))

        result = queries.create_listing(
            seller["login"],
            item_name,
            category,
            starting_price,
            item_condition=item_condition,
            description=description,
        )
        flash("Listing created.", "success")
        return redirect(url_for("seller.manage_auction", auction_id=result["auction_id"]))
    return render_template("pages/seller/create_listing.html", seller=seller)


@seller_bp.route("/sell/edit/<int:item_id>", methods=["GET", "POST"])
def edit_listing(item_id):
    seller = _current_seller()
    item = queries.get_item(item_id)
    if not item or item["seller_login"] != seller["login"]:
        abort(404)
    if request.method == "POST":
        queries.update_listing(
            item_id,
            seller["login"],
            item_name=request.form.get("item_name", "").strip(),
            category=request.form.get("category", "").strip(),
            starting_price=request.form.get("starting_price", type=float),
            item_condition=request.form.get("item_condition") or None,
            description=request.form.get("description") or None,
        )
        flash("Listing updated.", "success")
        return redirect(url_for("seller.listings"))
    return render_template("pages/seller/edit_listing.html", item=item, seller=seller)


@seller_bp.route("/sell/auction/<int:auction_id>/manage", methods=["GET", "POST"])
def manage_auction(auction_id):
    seller = _current_seller()
    auction = queries.get_auction_with_item(auction_id)
    if not auction or auction["seller_login"] != seller["login"]:
        abort(404)
    bids = queries.get_bids_for_auction(auction_id)
    if request.method == "POST" and request.form.get("action") == "end_auction":
        affected = queries.end_auction(auction_id, seller["login"])
        if affected:
            flash("Auction closed.", "success")
        else:
            flash("Could not close auction.", "error")
        return redirect(url_for("seller.manage_auction", auction_id=auction_id))
    return render_template(
        "pages/seller/manage_auction.html",
        auction=auction,
        bids=bids,
        seller=seller,
    )
