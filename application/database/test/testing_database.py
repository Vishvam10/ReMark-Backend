import sys
import os
import sqlite3
from flask import current_app, g
import logging
logging.basicConfig(stream=sys.stderr)
logging.getLogger("UserApiTestLogger").setLevel(logging.DEBUG)

def get_db():
    if "db" not in g:
        print("DEBUG : ", current_app.config["SQLALCHEMY_DATABASE_URI"])
        logger = logging.getLogger("UserApiTestLogger")
        logger.debug(current_app.config["SQLALCHEMY_DATABASE_URI"])
        g.db = sqlite3.connect(
            current_app.config["SQLALCHEMY_DATABASE_URI"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def init_db():
    db = get_db()

    with open(os.path.join(os.path.dirname(__file__), 'schema.sql'), 'rb') as f:
        db.executescript(f.read().decode("utf8"))

def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()