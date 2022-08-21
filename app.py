from multiprocessing.connection import wait
import os

from application.models.User import User
from application.models.Token import Token
from application.models.UserPreference import UserPreference
from application.models.Comment import Comment
from application.models.Annotation import Annotation
from application.models.Website import Website


from application import create_app

app, api, celery, cache = create_app(environment="DEVELOPMENT")

from application.specific_apis import login
from application.specific_apis import fileDownload
from application.base_apis.TokenAPI import *
from application.base_apis.WebsiteAPI import *
from application.base_apis.AnnotationAPI import *
from application.base_apis.CommentAPI import *
from application.base_apis.UserAPI import *
from application.base_apis.UserPreferenceAPI import *

from waitress import serve

if __name__ == "__main__" :
    # env = os.environ.get("FLASK_ENVIRONMENT", None)
    port = int(os.environ.get("PORT", 17995)) 
    # if(env == "DEVELOPMENT" or env == "TESTING") :
    print("APP ENVIRONMENT : ", os.environ.get("FLASK_ENVIRONMENT", None))
    print("APP INITIALIZED : ", app.config["SQLALCHEMY_DATABASE_URI"])
    app.run(host="0.0.0.0", port=port)
    # if(env == "PRODUCTION") :
    #     print("CONFIG : ", app.config["SQLALCHEMY_DATABASE_URI"], my_app)
    #     serve(my_app, port=port)