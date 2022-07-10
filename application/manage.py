from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from application.database import db

from flask import current_app as app

migrate = Migrate(app, db)