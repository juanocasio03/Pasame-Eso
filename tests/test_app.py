"""Smoke tests: pages load and access control works (NFR-SEC-04)."""
from conftest import login_as

# Seed data ids: 1 = moderator, 2 = contributor (see app/db.py seed_db)
MODERATOR_ID = 1
CONTRIBUTOR_ID = 2


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"PasameEso" in response.data


def test_public_pages_load(client):
    for path in ("/help", "/auth/login", "/auth/register", "/posts/1"):
        assert client.get(path).status_code == 200, path


def test_missing_post_is_404(client):
    assert client.get("/posts/9999").status_code == 404


def test_guest_cannot_create_post(client):
    response = client.get("/posts/new")
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_contributor_can_open_create_form(client):
    login_as(client, CONTRIBUTOR_ID)
    assert client.get("/posts/new").status_code == 200


def test_contributor_blocked_from_dashboard(client):
    login_as(client, CONTRIBUTOR_ID)
    assert client.get("/moderation/").status_code == 403


def test_moderator_sees_dashboard(client):
    login_as(client, MODERATOR_ID)
    response = client.get("/moderation/")
    assert response.status_code == 200
    assert b"Report queue" in response.data
