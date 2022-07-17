import uuid

from application.models.User import User
from application.models.Annotation import Annotation
from application.models.Comment import Comment

from application.utils.validation import BusinessValidationError
from application.utils.check_headers import check_headers

from application.database import db

from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import jsonify, request

comment_output_fields = {
    "comment_id" : fields.String,
    "annotation_id" : fields.String,
    "content" : fields.String,
    "content_html" : fields.String,

    "parent_node" : fields.String,

    "upvotes" : fields.Integer,
    "downvotes" : fields.Integer,
    
    "mod_required" : fields.Boolean,
    
    "created_at" : fields.DateTime,
    "updated_at" : fields.DateTime,

    "created_by" : fields.String
}

class CommentAPI(Resource):
    
    @jwt_required()
    @marshal_with(comment_output_fields)
    def get(self, comment_id) :
        check_headers(request=request)
        comment = db.session.query(Comment).filter(Comment.comment_id == comment_id).first()
        if(comment is None) :
            raise BusinessValidationError(status_code=400, error_message="Invalid comment ID")

        return comment

    @jwt_required()
    def post(self):
        check_headers(request=request)

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

    @jwt_required()
    @marshal_with(comment_output_fields)
    def put(self):       
        check_headers(request=request)

        data = request.json
        user_id = data["user_id"]
        comment_id = data["comment_id"]
        
        user = db.session.query(User).filter(User.user_id == user_id).first()

        if(user is None) :
            raise BusinessValidationError(status_code=400, error_message="Invalid user ID")

        comment = db.session.query(Comment).filter(Comment.comment_id == comment_id).first()

        if(comment is None) :
            raise BusinessValidationError(status_code=400, error_message="Invalid comment ID")

        if(comment.__dict__["created_by"] != user_id) :
            raise BusinessValidationError(status_code=409, error_message="Can not edit this comment as it is made by someone else")


        new_content = data["new_content"]
        new_content_html = data["new_content_html"]

        if new_content is None or new_content == "":
            raise BusinessValidationError(
                status_code=400, error_message="Content is required")
        if new_content_html is None or new_content_html == "":
            raise BusinessValidationError(
                status_code=400, error_message="HTML node data tag is required")

        comment.content = new_content
        comment.content_html = new_content_html

        print("************************ DEBUG ************************", comment)

        db.session.add(comment)
        db.session.commit()

        return comment

    @jwt_required()
    def delete(self, comment_id) :
        check_headers(request=request)

        # (FUTURE) Delete all replies as well

        comment = db.session.query(Comment).filter(Comment.comment_id == comment_id).first()
        if(comment is None) :
            raise BusinessValidationError(status_code=400, error_message="Invalid comment ID")
    
        db.session.query(Comment).filter(Comment.comment_id == comment_id).delete(synchronize_session=False)
        db.session.commit()

        return_value = {
            "message": "Comment deleted successfully",
            "comment_id": comment_id,
            "status": 200,
        }

        return jsonify(return_value)

