"""User model: registration, login and account management.

Requirements: REQ.1.1-1.3 (registration), REQ.2.1-2.3 (login),
FEAT-03 (account management), NFR-SEC-02/03 (hashing, lockout).
"""
import bcrypt

from ..db import get_db


class User:
    ROLES = ("contributor", "moderator")

    @staticmethod
    def hash_password(plain: str) -> str:
        """Salted bcrypt hash (NFR-SEC-02). Never store `plain` anywhere."""
        return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def check_password(plain: str, password_hash: str) -> bool:
        return bcrypt.checkpw(plain.encode("utf-8"), password_hash.encode("utf-8"))

    @staticmethod
    def get_by_id(user_id: int):
        return get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    @staticmethod
    def register(name: str, email: str, username: str, password: str):
        """REQ.1.1 / REQ.1.2: validate input and create a contributor account.

        TODO:
          - email must end in @upr.edu and be <= 64 chars
          - username <= 20 chars, letters/digits only
          - password 8-25 chars
          - reject duplicate email/username with a clear message (NFR-USE-03)
          - always create role='contributor' (FEAT-01)
          - use parameterized queries (?) only, never string formatting (SQL injection)
        Return the new user's id.
        """
        raise NotImplementedError

    @staticmethod
    def login(identifier: str, password: str):
        """REQ.2.2: verify email-or-username + password.

        TODO:
          - look up by email OR username
          - refuse inactive or locked accounts
          - on failure, increment failed_login_attempts; lock for 15 min after 5 (NFR-SEC-03)
          - on success, reset the counter
          - error text must not reveal which field was wrong
        Return the user row on success, None on failure.
        """
        raise NotImplementedError

    @staticmethod
    def deactivate(user_id: int):
        """FEAT-03: moderator deactivates an account. TODO"""
        raise NotImplementedError

    @staticmethod
    def delete(user_id: int):
        """FEAT-03: moderator deletes an account. TODO"""
        raise NotImplementedError
