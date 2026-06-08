from flask import Blueprint, render_template, request, redirect, url_for, flash

from data import queries

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
def dashboard():
    stats = queries.get_admin_stats()
    return render_template("pages/admin/dashboard.html", stats=stats)


@admin_bp.route("/admin/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        updated = 0
        for user in queries.get_all_users():
            new_role = request.form.get(f"role_{user['login']}")
            if new_role and new_role != user["role"]:
                queries.update_user_role(user["login"], new_role)
                updated += 1
        flash(f"Updated {updated} user role(s)." if updated else "No changes saved.", "success")
        return redirect(url_for("admin.users"))
    return render_template("pages/admin/users.html", users=queries.get_all_users())


@admin_bp.route("/admin/auctions")
def auctions():
    auctions_data = queries.get_all_auctions_enriched()
    return render_template("pages/admin/auctions.html", auctions=auctions_data)


@admin_bp.route("/admin/items", methods=["GET", "POST"])
def items():
    if request.method == "POST":
        item_id = request.form.get("remove_item", type=int)
        if item_id:
            try:
                affected = queries.remove_item(item_id)
                if affected:
                    flash("Item removed.", "success")
                else:
                    flash("Item not found.", "error")
            except Exception:
                flash("Could not remove item. It may have linked auctions or bids.", "error")
        return redirect(url_for("admin.items"))
    return render_template("pages/admin/items.html", items=queries.get_all_items())


@admin_bp.route("/admin/payments")
def payments():
    return render_template("pages/admin/payments.html", payments=queries.get_payments())


@admin_bp.route("/admin/shipments", methods=["GET", "POST"])
def shipments():
    if request.method == "POST":
        for shipment in queries.get_shipments():
            sid = shipment["shipment_id"]
            status = request.form.get(f"status_{sid}")
            tracking = request.form.get(f"tracking_{sid}") or None
            if status:
                queries.update_shipment(sid, status, tracking)
        flash("Shipments updated.", "success")
        return redirect(url_for("admin.shipments"))
    return render_template("pages/admin/shipments.html", shipments=queries.get_shipments())
