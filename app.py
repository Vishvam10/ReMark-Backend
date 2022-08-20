from application.models.User import User
from application.models.Token import Token
from application.models.UserPreference import UserPreference
from application.models.Comment import Comment
from application.models.Annotation import Annotation
from application.models.Website import Website


from application import create_app

app, api, celery, cache = create_app()

from application.specific_apis import login
from application.specific_apis import fileDownload
from application.base_apis.TokenAPI import *
from application.base_apis.WebsiteAPI import *
from application.base_apis.AnnotationAPI import *
from application.base_apis.CommentAPI import *
from application.base_apis.UserAPI import *
from application.base_apis.UserPreferenceAPI import *

if __name__ == "__main__" :
    app.run(host='0.0.0.0', debug=True)
