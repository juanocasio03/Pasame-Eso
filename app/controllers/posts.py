"""Resources: create (Screen 3), view (Screen 4), edit, rate, comment, report.

Requirements: REQ.4.x, FEAT-06, FEAT-07, REQ.5.1.
"""
from flask import Blueprint, abort, flash, render_template, request

from ..models import Post, Report
from .decorators import login_required

bp = Blueprint("posts", __name__, url_prefix="/posts")


@bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        # TODO (REQ.4.1-4.3): read form + request.files["file"], call Post.create(),
        # show duplicate/validation errors, redirect to posts.view on success.
        flash("Uploading is not implemented yet.")
    return render_template(
        "posts/create.html", resource_types=Post.RESOURCE_TYPES
    )


@bp.route("/<int:post_id>")
def view(post_id):
    post = Post.get_by_id(post_id)
    if post is None:
        abort(404)
    # TODO: load average rating, the user's rating and comments.
    return render_template("posts/view.html", post=post, reasons=Report.REASONS)


@bp.route("/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit(post_id):
    # TODO (FEAT-04): only the owner or a moderator may edit.
    abort(501)


@bp.route("/<int:post_id>/rate", methods=["POST"])
@login_required
def rate(post_id):
    # TODO (FEAT-06): Post.rate(post_id, g.user["id"], stars)
    abort(501)


@bp.route("/<int:post_id>/comment", methods=["POST"])
@login_required
def comment(post_id):
    # TODO (FEAT-07): Post.comment(post_id, g.user["id"], body)
    abort(501)


@bp.route("/<int:post_id>/report", methods=["POST"])
@login_required
def report(post_id):
    # TODO (REQ.5.1): Report.create(post_id, g.user["id"], reason, description)
    abort(501)
