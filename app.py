from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

# from application import workers
from application.config import LocalDevelopmentConfig

from application.database import db
# from application.manage import *
from application.models import Annotation
from application.models import User
from application.models import Website

from flask_cors import CORS
# from flask_caching import Cache

# from flask_jwt_extended import JWTManager
# from waitress import serve

app = None
api = None
celery = None
cache = None

migrate = Migrate()

def create_app() :
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)

    # jwt = JWTManager(app)    
    # app.app_context().push()
    
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


app, api, celery, cache = create_app()

# from application.specific_apis import *
from application.base_apis.UserAPI import *

# from application.specific_apis import dummy_api

api.add_resource(UserAPI, "/api/user", "/api/user/<string:user_id>")
# api.add_resource(DeckAPI, "/api/deck", "/api/deck/<string:deck_id>")
# api.add_resource(CardAPI, "/api/card", "/api/card/<string:deck_id>")
# api.add_resource(ReviewAPI, "/api/review/<string:deck_id>")

if __name__ == '__main__':
    app.run(host='0.0.0.0')