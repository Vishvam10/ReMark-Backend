from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

# from application import workers
from application.config import LocalDevelopmentConfig, LocalTestingConfig

from application.database.dev.database import db
from flask_cors import CORS
# from flask_caching import Cache

from flask_jwt_extended import JWTManager
# from waitress import serve

app = None
api = None
celery = None
cache = None

migrate = Migrate()

def create_app(environment="dev"):
    app = Flask(__name__)
    
    if(environment == "testing"):
        app.config.from_object(LocalTestingConfig)
    else:
        app.config.from_object(LocalDevelopmentConfig)

    jwt = JWTManager(app)
    app.app_context().push()

    db.init_app(app)
    app.app_context().push()

    migrate.init_app(app, db)
    app.app_context().push()

    CORS(app)
    app.app_context().push()

    api = Api(app)
    app.app_context().push()

    # Create celery
    # celery = workers.celery

    # Update with configuration
    # celery.conf.update(
    # broker_url = app.config["CELERY_BROKER_URL"],
    # result_backend = app.config["CELERY_RESULT_BACKEND"],
    # )

    # celery.Task = workers.ContextTask
    # app.app_context().push()

    # cache = Cache(app)
    # app.app_context().push()

    return app, api, celery, cache

