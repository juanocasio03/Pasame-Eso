"""PasameEso application factory.

`create_app()` builds and configures the Flask app. Every part of the system
plugs in here: configuration, the database, and the controllers (blueprints).
"""
import os

from flask import Flask

from . import db
from .config import Config


def create_app(config_overrides=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if config_overrides:
        app.config.update(config_overrides)

    # The instance/ folder holds local, never-committed data: the SQLite file
    # and uploaded resources. Create it (and uploads/) if it doesn't exist.
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)

    # Controllers (the "C" in MVC). One blueprint per feature area.
    from .controllers import auth, main, moderation, posts

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(posts.bp)
    app.register_blueprint(moderation.bp)

    return app
