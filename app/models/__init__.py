"""Models (the "M" in MVC): data and business logic.

Each class matches the UML structural model in System Design Section 3.2.
Controllers call these methods; models talk to the database through db.get_db().
Methods marked TODO are yours to implement, one issue/branch at a time.
"""
from .post import Post
from .report import Report
from .user import User

__all__ = ["User", "Post", "Report"]
