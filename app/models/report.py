"""Report model: flag content and the moderator queue.

Requirements: REQ.5.1 (submit), REQ.5.2 (queue), REQ.5.3 (resolve).
See the sequence diagram in System Design Fig. 3.3.
"""
from ..db import get_db


class Report:
    REASONS = {
        "inappropriate": "Inappropriate content",
        "incorrect": "Incorrect information",
        "plagiarism": "Plagiarism",
        "duplicate": "Duplicate",
        "other": "Other",
    }
    ACTIONS = ("keep", "edit", "delete")

    @staticmethod
    def create(post_id: int, reporter_id: int, reason: str, description: str = ""):
        """REQ.5.1: one report per user per post; description required if reason='other'. TODO"""
        raise NotImplementedError

    @staticmethod
    def list_queue():
        """REQ.5.2: posts with pending reports, most-reported first, then newest report.

        Starting point for the query (returns title, course, count, latest date):
        """
        return get_db().execute(
            """
            SELECT p.id, p.title, p.course_code,
                   COUNT(r.id)       AS report_count,
                   MAX(r.created_at) AS latest_report
            FROM reports r
            JOIN posts p ON p.id = r.post_id
            WHERE r.status != 'resolved'
            GROUP BY p.id
            ORDER BY report_count DESC, latest_report DESC
            """
        ).fetchall()

    @staticmethod
    def resolve(post_id: int, moderator_id: int, action: str, note: str = ""):
        """REQ.5.3: apply keep/edit/delete, mark reports resolved, log the action.

        TODO: do it in ONE transaction so a failure leaves nothing half-done.
        """
        raise NotImplementedError
