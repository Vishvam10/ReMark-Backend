import uuid

from application.models.Annotation import Annotation
from application.models.Comment import Comment

from application.utils.validation import BusinessValidationError

from application.database import db

from flask_restful import Resource
from flask import jsonify, request


class CommentAPI(Resource):
    def get(self, annotation_id) :
        annotation = db.session.query(Annotation).filter(Annotation.annotation_id == annotation_id).first()
        if(annotation is None) :
            raise BusinessValidationError(status_code=400, error_message="Invalid annotation ID")

        print("****************************** COMMENTS *******************************", annotation.comments)       
        return_value = {
            "message": "New Comment Created",
            "status": 201,
            "data" : {
                "comments" : annotation.comments
            }
        }
        return jsonify(return_value)

    def post(self):
        comment_id = str(uuid.uuid4()).replace("-", "")
        
        data = request.json
        
        annotation_id = data["annotation_id"]
        content = data["content"]
        content_html = data["content_html"]
        parent_node = data["parent_node"]
        created_by = data["created_by"]

        upvotes = 0
        downvotes = 0
        mod_required = False
        
        if created_by is None or created_by == "":
            raise BusinessValidationError(
                status_code=400, error_message="User ID is required")
        if content is None or content == "":
            raise BusinessValidationError(
                status_code=400, error_message="Content is required")
        if content_html is None or content_html == "":
            raise BusinessValidationError(
                status_code=400, error_message="HTML node data tag is required")


        new_comment = Comment(comment_id=comment_id, annotation_id=annotation_id, content=content, content_html=content_html, parent_node=parent_node, upvotes=upvotes, downvotes=downvotes, mod_required=mod_required, created_by=created_by)

        db.session.add(new_comment)
        db.session.commit()

        return_value = {
            "message": "New Comment Created",
            "status": 201,
            "data" : {
                "created_by": created_by,
                "comment_id": comment_id,
                "content" : content,
                "content_html" : content_html,
                "created_by" : created_by
            }
        }

        return jsonify(return_value)

    # @marshal_with(annotation_output_fields)
    # def put(self, annotation_id) :
    #     data = request.json

    #     user_id = data["user_id"]
    #     content = data["content"]
    #     html_content = data["html_content"]
    #     tags = data["tags"]

    #     if user_id is None or user_id == "":
    #         raise BusinessValidationError(
    #             status_code=400, error_message="User ID is required")
    #     if content is None or content == "":
    #         raise BusinessValidationError(
    #             status_code=400, error_message="Content is required")
    #     if html_content is None or html_content == "":
    #         raise BusinessValidationError(
    #             status_code=400, error_message="HTML content is required")

    #     annotation = db.session.query(Annotation).filter(Annotation.annotation_id == annotation_id).first()
    #     user = db.session.query(User).filter(User.user_id == user_id).first()
        
    #     if(annotation is None):
    #         raise BusinessValidationError(status_code=400, error_message="Invalid annotation ID or no such annotation exists")
    #     if(user is None):
    #         raise BusinessValidationError(status_code=400, error_message="Invalid annotation ID or no such annotation exists")

    #     annotation.content = content
    #     annotation.html_content = html_content
    #     annotation.tags = tags
    #     annotation.modified_by = user_id

    #     db.session.add(annotation)
    #     db.session.commit()
    #     return annotation

    # def delete(self, annotation_id) :
    #     # 1. Delete all replies

    #     # 2. Delete the annotation
    #     # db.session.query(Annotation).filter(Annotation.annotation_id == annotation_id).delete(synchronize_session=False)
    #     # db.session.commit()

    #     return_value = {
    #         "annotation_id": annotation_id,
    #         "message": "Annotation deleted successfully",
    #         "status": 200,
    #     }

    #     return jsonify(return_value)

