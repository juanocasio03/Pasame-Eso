"""Database access layer (SQLite via Python's sqlite3 module, SI-01).

Use `get_db()` inside any request to get a connection. It is opened once per
request and closed automatically at the end.

Command-line helpers (run from the project root):
    flask --app app init-db    # create an empty database from schema.sql
    flask --app app seed-db    # add sample users and posts for local testing
"""
import sqlite3

import click
from flask import current_app, g


def get_db():
    if "db" not in g:
        # Timestamps come back as "YYYY-MM-DD HH:MM:SS" strings (UTC).
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row  # rows behave like dicts: row["title"]
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


def seed_db():
    """Insert sample data so everyone has the same starting point locally."""
    import bcrypt

    db = get_db()

    def pw(plain):
        return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

    db.executemany(
        "INSERT INTO users (name, email, username, password_hash, role)"
        " VALUES (?, ?, ?, ?, ?)",
        [
            ("Mod Erador", "mod.erador@upr.edu", "moderator", pw("moderator123"), "moderator"),
            ("Ana Estudiante", "ana.estudiante@upr.edu", "ana", pw("contributor123"), "contributor"),
        ],
    )
    db.executemany(
        "INSERT INTO posts (user_id, title, resource_type, course_code, course_name,"
        " professor, description, file_path, file_hash, file_mime, file_size)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [
            (2, "Notas parcial 1", "class_notes", "CCOM4030", "Ingenieria de Software",
             "Prof. Ejemplo", "Notas de los temas 1-4.", "seed/notas.pdf",
             "seed-hash-1", "application/pdf", 1024),
            (2, "Examen de practica", "practice_exam", "MATE3031", "Calculo I",
             "Prof. Ejemplo", "Examen viejo con soluciones.", "seed/examen.pdf",
             "seed-hash-2", "application/pdf", 2048),
        ],
    )
    db.commit()


@click.command("init-db")
def init_db_command():
    """Drop all tables and recreate them from schema.sql."""
    init_db()
    click.echo("Initialized the database.")


@click.command("seed-db")
def seed_db_command():
    """Fill the database with sample data (run init-db first)."""
    seed_db()
    click.echo("Seeded the database. Logins: moderator/moderator123, ana/contributor123")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
