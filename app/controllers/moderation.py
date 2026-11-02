"""Moderator dashboard (Screen 5): report queue and resolving reports.

Requirements: REQ.5.2, REQ.5.3, FEAT-03. Every route here is moderator-only.
"""
from flask import Blueprint, abort, render_template

from ..models import Report
from .decorators import moderator_required

bp = Blueprint("moderation", __name__, url_prefix="/moderation")


@bp.route("/")
@moderator_required
def dashboard():
    queue = Report.list_queue()
    return render_template("moderation/dashboard.html", queue=queue)


@bp.route("/posts/<int:post_id>/resolve", methods=["POST"])
@moderator_required
def resolve(post_id):
    # TODO (REQ.5.3): Report.resolve(post_id, g.user["id"], action, note)
    abort(501)


@bp.route("/accounts")
@moderator_required
def accounts():
    # TODO (FEAT-03, UI-03): searchable list of accounts with deactivate/delete.
    abort(501)
