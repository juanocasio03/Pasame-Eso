"""Shared test setup: every test gets a fresh app with a temporary database."""
import os
import tempfile

import pytest

from app import create_app
from app.db import init_db, seed_db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    upload_dir = tempfile.mkdtemp()
    app = create_app({
        "TESTING": True,
        "DATABASE": db_path,
        "UPLOAD_FOLDER": upload_dir,
        "SECRET_KEY": "test",
    })
    with app.app_context():
        init_db()
        seed_db()
    yield app
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


def login_as(client, user_id):
    """Log a test client in without going through the login form."""
    with client.session_transaction() as sess:
        sess["user_id"] = user_id
