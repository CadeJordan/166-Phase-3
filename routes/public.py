from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort

from data import queries

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def home():
    auctions = queries.search_auctions()
    return render_template("pages/public/browse.html", auctions=auctions)


@public_bp.route("/search")
def search():
    q = request.args.get("q", "")
    auctions = queries.search_auctions(q=q)
    return render_template("pages/public/search.html", auctions=auctions, query=q)


@public_bp.route("/auction/<int:auction_id>", methods=["GET", "POST"])
def auction_detail(auction_id):
    auction = queries.get_auction_with_item(auction_id)
    if not auction:
        abort(404)

    if request.method == "POST":
        login = session.get("demo_user")
        if not login:
            flash("Sign in to place a bid.", "error")
            return redirect(url_for("auth.login"))

        if session.get("demo_role") != "Buyer":
            flash("Only buyers can place bids.", "error")
            return redirect(url_for("public.auction_detail", auction_id=auction_id))

        bid_amount = request.form.get("bid_amount", type=float)
        if bid_amount is None:
            flash("Enter a valid bid amount.", "error")
            return redirect(url_for("public.auction_detail", auction_id=auction_id))

        try:
            placed = queries.place_bid(auction_id, login, bid_amount)
        except Exception:
            placed = False

        if placed:
            flash("Bid placed.", "success")
        else:
            flash(
                "Bid rejected. Amount must exceed the current bid and the auction must be active.",
                "error",
            )
        return redirect(url_for("public.auction_detail", auction_id=auction_id))

    bids = queries.get_bids_for_auction(auction_id)
    return render_template(
        "pages/public/auction_detail.html",
        auction=auction,
        bids=bids,
    )
