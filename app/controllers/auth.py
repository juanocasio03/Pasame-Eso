"""Register, login, logout (Screen 1, REQ.1.x and REQ.2.x)."""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

bp = Blueprint("auth", __name__, url_prefix="/auth")


def start_session(user_id: int):
    """REQ.1.3 / REQ.2.3: log the user in. 30-minute timeout comes from config."""
    session.clear()
    session.permanent = True
    session["user_id"] = user_id


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # TODO (REQ.1.1-1.3):
        #   user_id = User.register(name, email, username, password)
        #   start_session(user_id); return redirect(url_for("main.index"))
        flash("Registration is not implemented yet.")
    return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # TODO (REQ.2.1-2.3):
        #   user = User.login(identifier, password)
        #   if user: start_session(user["id"]); redirect to `next` or home
        #   else: flash("The email/username or password is incorrect.")
        flash("Login is not implemented yet.")
    return render_template("auth/login.html")


@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("main.index"))
