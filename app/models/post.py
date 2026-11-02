"""Post (resource) model: upload, edit, search, rate, comment.

Requirements: REQ.3.x (search), REQ.4.1-4.3 (upload + duplicate detection),
FEAT-06 (rating), FEAT-07 (comments).
"""
from ..db import get_db


class Post:
    RESOURCE_TYPES = {
        "class_notes": "Class Notes",
        "practice_exam": "Practice Exam",
        "study_guide": "Study Guide",
    }

    @staticmethod
    def get_by_id(post_id: int):
        return get_db().execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()

    @staticmethod
    def find_duplicate(course_code: str, file_hash: str):
        """REQ.4.2: return an existing post with the same file in the same course, or None."""
        return get_db().execute(
            "SELECT id, title FROM posts WHERE course_code = ? AND file_hash = ?",
            (course_code, file_hash),
        ).fetchone()

    @staticmethod
    def create(user_id, title, resource_type, course_code, course_name,
               professor, description, file_storage):
        """REQ.4.1-4.3: validate, check duplicates, store file + row, return post id.

        TODO, following the process model (System Design Fig. 3.1):
          1. validate fields (title <= 100, course code format, type in RESOURCE_TYPES)
          2. utils.files.detect_file_type() on the content (NFR-SEC-06)
          3. utils.files.sha256_of() -> find_duplicate(); if found, return/raise with a link
          4. save the file under UPLOAD_FOLDER with a generated name (never the user's filename)
          5. INSERT the row; if the INSERT fails, delete the saved file so nothing is
             half-created (NFR-REL-05)
        """
        raise NotImplementedError

    @staticmethod
    def edit(post_id: int, editor_id: int, **fields):
        """FEAT-04: owner (or moderator) edits title/description/etc. TODO"""
        raise NotImplementedError

    @staticmethod
    def delete(post_id: int):
        """Delete the row AND its stored file together. TODO"""
        raise NotImplementedError

    @staticmethod
    def search(course_code=None, professor=None, course_name=None,
               resource_type=None, date_from=None, min_rating=None, page=1):
        """REQ.3.1-3.3: filtered search. With no filters, return the most popular posts.

        TODO: build the WHERE clause from the filters that are set, join the average
        rating, order by your ranking, and paginate (NFR-PERF-03).
        """
        raise NotImplementedError

    @staticmethod
    def rate(post_id: int, user_id: int, stars: int):
        """FEAT-06: insert or update the user's 1-5 star rating. TODO"""
        raise NotImplementedError

    @staticmethod
    def comment(post_id: int, user_id: int, body: str):
        """FEAT-07: add a plain-text comment. TODO"""
        raise NotImplementedError
