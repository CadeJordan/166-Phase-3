from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort

from data import queries

buyer_bp = Blueprint("buyer", __name__)


def _current_user():
    login = session.get("demo_user", "buyer1")
    return queries.get_user(login) or queries.get_user("buyer1")


@buyer_bp.route("/account", methods=["GET", "POST"])
def account():
    user = _current_user()
    if request.method == "POST":
        phone_num = request.form.get("phone_num", "").strip()
        address = request.form.get("address", "").strip()
        if not phone_num or not address:
            flash("Phone and address are required.", "error")
            return redirect(url_for("buyer.account"))
        queries.update_user_profile(user["login"], phone_num, address, user.get("favorite_category"))
        flash("Profile updated.", "success")
        return redirect(url_for("buyer.account"))
    return render_template("pages/buyer/account.html", user=user)


@buyer_bp.route("/bids")
def bids():
    user = _current_user()
    bids = queries.get_user_bids(user["login"])
    return render_template("pages/buyer/my_bids.html", bids=bids, user=user)


@buyer_bp.route("/wins")
def wins():
    user = _current_user()
    wins = queries.get_user_wins(user["login"])
    return render_template("pages/buyer/my_wins.html", wins=wins, user=user)


@buyer_bp.route("/payment/<int:auction_id>", methods=["GET", "POST"])
def payment(auction_id):
    user = _current_user()
    auction = queries.get_auction_with_item(auction_id)
    if not auction:
        abort(404)
    payment_record = queries.get_payment_for_auction(auction_id)
    if request.method == "POST":
        affected = queries.process_payment(auction_id, user["login"])
        if affected:
            flash("Payment completed.", "success")
        else:
            flash("Payment failed. You must be the winner of a closed auction.", "error")
        return redirect(url_for("buyer.payment", auction_id=auction_id))
    return render_template(
        "pages/buyer/payment.html",
        auction=auction,
        payment=payment_record,
    )


@buyer_bp.route("/orders/<int:auction_id>")
def order_tracking(auction_id):
    auction = queries.get_auction_with_item(auction_id)
    if not auction:
        abort(404)
    shipment = queries.get_shipment_for_auction(auction_id)
    payment_record = queries.get_payment_for_auction(auction_id)
    return render_template(
        "pages/buyer/order_tracking.html",
        auction=auction,
        shipment=shipment,
        payment=payment_record,
    )
