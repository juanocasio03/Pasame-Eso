"""Central configuration (NFR-PORT-04).

All environment-specific settings are read from environment variables, which
you set in a local `.env` file (copy `.env.example`). Moving to another host
should only require changing `.env`, never the code.
"""
import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")


class Config:
    # Signs session cookies. MUST be a long random value outside development.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")

    # SQLite database file (DEP-03, SI-01).
    DATABASE = os.environ.get(
        "DATABASE_PATH", os.path.join(INSTANCE_DIR, "pasameeso.sqlite")
    )

    # Where uploaded resource files are stored (SI-02).
    UPLOAD_FOLDER = os.environ.get(
        "UPLOAD_FOLDER", os.path.join(INSTANCE_DIR, "uploads")
    )

    # Max upload size: 25 MB (NFR-PERF-04). Flask rejects bigger requests.
    MAX_UPLOAD_MB = int(os.environ.get("MAX_UPLOAD_MB", 25))
    MAX_CONTENT_LENGTH = MAX_UPLOAD_MB * 1024 * 1024

    # Sessions expire after 30 minutes of inactivity (NFR-SEC-05).
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    # Turn on in production, where the site runs over HTTPS (NFR-SEC-01).
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "0") == "1"

    # Login lockout (NFR-SEC-03).
    MAX_FAILED_LOGINS = 5
    LOCKOUT_MINUTES = 15

    # Only institutional emails may register (ASSUME-01).
    ALLOWED_EMAIL_DOMAIN = "upr.edu"
