"""Server-side access control (NFR-SEC-04).

Put these on any route that needs them. Hiding a button in the HTML is NOT
security; these checks are what actually block unauthorized requests.

    @bp.route("/create")
    @login_required
    def create(): ...

    @bp.route("/dashboard")
    @moderator_required
    def dashboard(): ...
"""
from functools import wraps

from flask import abort, flash, g, redirect, request, session, url_for

from ..models import User


def load_current_user():
    """Run before every request: sets g.user to the logged-in user row or None."""
    user_id = session.get("user_id")
    g.user = User.get_by_id(user_id) if user_id else None
    if g.user is not None and not g.user["is_active"]:
        session.clear()
        g.user = None


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if g.user is None:
            flash("Please log in to continue.")
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def moderator_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.login", next=request.path))
        if g.user["role"] != "moderator":
            abort(403)
        return view(*args, **kwargs)
    return wrapped
