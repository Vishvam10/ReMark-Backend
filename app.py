from application.models.User import *
from application.models.Comment import *
from application.models.Annotation import *
from application.models.Website import *

from application import create_app

app, api, celery, cache = create_app()

from application.specific_apis import login
from application.specific_apis import fileDownload
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
