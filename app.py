from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

# from application import workers
from application.config import LocalDevelopmentConfig, LocalTestingConfig

from application.database.database import db

from application.models.User import *
from application.models.Comment import *
from application.models.Annotation import *
from application.models.Website import *

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


app, api, celery, cache = create_app()

from application.specific_apis import login
from application.specific_apis import dummy
from application.base_apis.TokenAPI import *
from application.base_apis.WebsiteAPI import *
from application.base_apis.AnnotationAPI import *
from application.base_apis.CommentAPI import *
from application.base_apis.UserAPI import *

api.add_resource(UserAPI, "/api/user", "/api/user/<string:user_id>")
api.add_resource(AnnotationAPI, "/api/annotation",
                    "/api/annotation/<string:annotation_id>")
api.add_resource(CommentAPI, "/api/comment",
                    "/api/comment/<string:comment_id>")
api.add_resource(WebsiteAPI, "/api/website",
                    "/api/website/<string:website_id>")
api.add_resource(TokenAPI, "/api/token/<string:user_id>")

if __name__ == "__main__" :
    app.run(host='0.0.0.0', debug=True)
