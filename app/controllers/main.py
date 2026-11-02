"""Home feed + search (Screen 2, REQ.3.x) and the help page (NFR-USE-04)."""
from flask import Blueprint, render_template, request

from .decorators import load_current_user

bp = Blueprint("main", __name__)


@bp.before_app_request
def before_request():
    load_current_user()


@bp.route("/")
def index():
    filters = {
        "q": request.args.get("q", "").strip(),
        "course_code": request.args.get("course", "").strip().upper(),
        "professor": request.args.get("professor", "").strip(),
        "resource_type": request.args.get("type", ""),
    }
    # TODO (REQ.3.2): posts = Post.search(**filters)
    posts = []
    return render_template("index.html", posts=posts, filters=filters)


@bp.route("/help")
def help_page():
    return render_template("help.html")
