from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from data import queries

auth_bp = Blueprint("auth", __name__)


def _stub_post_redirect():
    flash("UI only — SQL backend not connected.", "info")
    return redirect(request.referrer or url_for("public.home"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        demo_user = request.form.get("demo_user", "")
        user = queries.get_user(demo_user)
        if user:
            session["demo_user"] = user["login"]
            session["demo_role"] = user["role"]
            flash(f"Signed in as {user['login']} ({user['role']})", "success")
            return redirect(url_for("public.home"))
        flash("Please select a demo user.", "error")
        return redirect(url_for("auth.login"))

    return render_template("pages/auth/login.html", users=queries.get_all_users())


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return _stub_post_redirect()
    return render_template("pages/auth/register.html")


@auth_bp.route("/logout")
def logout():
    session.pop("demo_user", None)
    session.pop("demo_role", None)
    flash("Signed out.", "info")
    return redirect(url_for("public.home"))
