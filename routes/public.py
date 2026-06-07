from flask import Blueprint, render_template, request, abort

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


@public_bp.route("/auction/<int:auction_id>")
def auction_detail(auction_id):
    auction = queries.get_auction_with_item(auction_id)
    if not auction:
        abort(404)
    bids = queries.get_bids_for_auction(auction_id)
    return render_template(
        "pages/public/auction_detail.html",
        auction=auction,
        bids=bids,
    )
