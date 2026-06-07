from flask import Blueprint, render_template, request, redirect, url_for, flash

from data import queries

admin_bp = Blueprint("admin", __name__)


def _stub_post_redirect():
    flash("UI only — SQL backend not connected.", "info")
    return redirect(request.referrer or url_for("admin.dashboard"))


@admin_bp.route("/admin")
def dashboard():
    stats = queries.get_admin_stats()
    return render_template("pages/admin/dashboard.html", stats=stats)


@admin_bp.route("/admin/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        return _stub_post_redirect()
    return render_template("pages/admin/users.html", users=queries.get_all_users())


@admin_bp.route("/admin/auctions")
def auctions():
    auctions_data = queries.get_all_auctions_enriched()
    return render_template("pages/admin/auctions.html", auctions=auctions_data)


@admin_bp.route("/admin/items", methods=["GET", "POST"])
def items():
    if request.method == "POST":
        return _stub_post_redirect()
    return render_template("pages/admin/items.html", items=queries.get_all_items())


@admin_bp.route("/admin/payments")
def payments():
    return render_template("pages/admin/payments.html", payments=queries.get_payments())


@admin_bp.route("/admin/shipments", methods=["GET", "POST"])
def shipments():
    if request.method == "POST":
        return _stub_post_redirect()
    return render_template("pages/admin/shipments.html", shipments=queries.get_shipments())
