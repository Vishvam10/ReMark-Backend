from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask import Blueprint

# from application import workers
from application.config import LocalDevelopmentConfig, LocalTestingConfig, ProductionConfig

from application.database.database import db
from flask_cors import CORS
# from flask_caching import Cache

from flask_jwt_extended import JWTManager
# from waitress import serve

app = None
api = None
celery = None
cache = None

migrate = Migrate()

import os
env = os.environ.get('ENV', None)

def create_app():
    app = Flask(__name__)
    
    if(env == "TESTING"):
        app.config.from_object(LocalTestingConfig)
    elif(env == "PRODUCTION"):
        app.config.from_object(ProductionConfig)
    else :
        app.config.from_object(LocalDevelopmentConfig)

    jwt = JWTManager(app)
    app.app_context().push()

    db.init_app(app)
    app.app_context().push()

    migrate.init_app(app, db)
    app.app_context().push()

    CORS(app)
    app.app_context().push()

    from application.models.User import User
    from application.models.Token import Token
    from application.models.UserPreference import UserPreference
    from application.models.Comment import Comment
    from application.models.Annotation import Annotation
    from application.models.Website import Website

    from application.specific_apis import login
    from application.specific_apis import fileDownload
    from application.base_apis.TokenAPI import TokenAPI
    from application.base_apis.WebsiteAPI import WebsiteAPI
    from application.base_apis.WebsiteAPI import website_extras
    from application.base_apis.AnnotationAPI import AnnotationAPI
    from application.base_apis.AnnotationAPI import annotation_extras
    from application.base_apis.CommentAPI import CommentAPI
    from application.base_apis.UserAPI import UserAPI
    from application.base_apis.UserAPI import user_extras
    from application.base_apis.UserPreferenceAPI import UserPreferenceAPI



    api_bp = Blueprint('/api/', __name__)
    api = Api(api_bp)
    
    api.add_resource(UserAPI, "/api/user", "/api/user/<string:user_id>")
    api.add_resource(UserPreferenceAPI, "/api/user_preference/<string:user_id>")
    api.add_resource(AnnotationAPI, "/api/annotation",
                        "/api/annotation/<string:annotation_id>")
    api.add_resource(CommentAPI, "/api/comment",
                        "/api/comment/<string:comment_id>")
    api.add_resource(WebsiteAPI, "/api/website",
                        "/api/website/<string:website_id>")
    api.add_resource(TokenAPI, "/api/token/<string:user_id>")

    app.register_blueprint(api_bp)
    app.register_blueprint(website_extras)
    app.register_blueprint(annotation_extras)
    app.register_blueprint(user_extras)
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

