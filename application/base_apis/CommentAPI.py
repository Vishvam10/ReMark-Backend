import datetime
import uuid

from application.models.User import User
from application.models.Comment import Comment

from application.utils.validation import BusinessValidationError
from application.utils.check_headers import check_headers

from application.database.database import db

from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import jsonify, request

from flask import current_app as app

comment_output_fields = {
    "comment_id": fields.String,
    "annotation_id": fields.String,
    "content": fields.String,
    "content_html": fields.String,

    "parent_node": fields.String,

    "upvotes": fields.Integer,
    "downvotes": fields.Integer,

    "mod_required": fields.Boolean,

    "created_at": fields.DateTime,
    "updated_at": fields.DateTime,

    "created_by_id": fields.String,
    "created_by": fields.String
}


class CommentAPI(Resource):

    @jwt_required()
    @marshal_with(comment_output_fields)
    def get(self, comment_id):
        check_headers(request=request)
        comment = db.session.query(Comment).filter(
            Comment.comment_id == comment_id).first()
        if(comment is None):
            raise BusinessValidationError(
                status_code=400, error_message="Invalid comment ID")

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
        user_id = data["user_id"]
        user_name = data["user_name"]

        upvotes = 0
        downvotes = 0
        mod_required = False

        if user_id is None or user_id == "":
            raise BusinessValidationError(
                status_code=400, error_message="User ID is required")
        if user_name is None or user_name == "":
            raise BusinessValidationError(
                status_code=400, error_message="Username is required")
        if content is None or content == "":
            raise BusinessValidationError(
                status_code=400, error_message="Content is required")

        new_comment = Comment(comment_id=comment_id, annotation_id=annotation_id, content=content, content_html=content_html,
                              parent_node=parent_node, upvotes=upvotes, downvotes=downvotes, mod_required=mod_required, created_by=user_name, created_by_id=user_id)

        now = datetime.datetime.now().strftime("%c")

        db.session.add(new_comment)
        db.session.commit()

        return_value = {
            "message": "New Comment Created",
            "status": 201,
            "data": {
                "created_by_id": user_id,
                "created_by": user_name,
                "created_at": now,
                "comment_id": comment_id,
                "content": content,
                "content_html": content_html,
                "upvotes": upvotes,
                "downvotes": downvotes,
                "mod_required": mod_required,
            }
        }

        return jsonify(return_value)

    @jwt_required()
    @marshal_with(comment_output_fields)
    def put(self, comment_id):
        check_headers(request=request)

        data = request.json
        user_id = data["user_id"]

        user = db.session.query(User).filter(User.user_id == user_id).first()

        if(user is None):
            raise BusinessValidationError(
                status_code=400, error_message="Invalid user ID")

        comment = db.session.query(Comment).filter(
            Comment.comment_id == comment_id).first()

        if(comment is None):
            raise BusinessValidationError(
                status_code=400, error_message="Invalid comment ID")

        if(comment.__dict__["created_by_id"] != user_id):
            error_message = "Can not edit this comment as it is made by someone else"
            raise BusinessValidationError(
                status_code=409, error_message=error_message)

        new_content = data["new_content"]
        new_content_html = data["new_content_html"]

        if new_content is None or new_content == "":
            raise BusinessValidationError(
                status_code=400, error_message="Content is required")

        comment.content = new_content
        comment.content_html = new_content_html

        db.session.add(comment)
        db.session.commit()

        return comment

    @jwt_required()
    def delete(self, comment_id):
        check_headers(request=request)

        # (FUTURE) Delete all replies as well

        comment = db.session.query(Comment).filter(
            Comment.comment_id == comment_id).first()
        if(comment is None):
            raise BusinessValidationError(
                status_code=400, error_message="Invalid comment ID")

        db.session.query(Comment).filter(Comment.comment_id ==
                                         comment_id).delete(synchronize_session=False)
        db.session.commit()

        return_value = {
            "message": "Comment deleted successfully",
            "comment_id": comment_id,
            "status": 200,
        }

        return jsonify(return_value)


@app.route('/api/comment/vote/<string:comment_id>', methods=["PUT"])
def update_vote(comment_id):

    data = request.json
    action_type = data["action_type"]
    user_id = data["user_id"]

    user = db.session.query(User).filter(User.user_id == user_id).first()
    comment = db.session.query(Comment).filter(
        Comment.comment_id == comment_id).first()

    if(user is None):
        raise BusinessValidationError(
            status_code=400, error_message="Invalid user ID")

    if(comment is None):
        raise BusinessValidationError(
            status_code=400, error_message="Invalid comment")

    user_upvotes = user.__dict__["upvotes"]
    user_downvotes = user.__dict__["downvotes"]

    if(action_type == "upvote"):
        if(comment_id in user_upvotes):
            raise BusinessValidationError(
                status_code=400, error_message="Already upvoted")

        if(comment_id in user_downvotes):
            user_downvotes = user_downvotes.replace(comment_id, "")
            user_downvotes += "," + user_downvotes

            user.downvotes = user_downvotes
            comment.downvotes -= 1

        user_upvotes += "," + comment_id

        user.upvotes = user_upvotes
        comment.upvotes = comment.upvotes + 1

        db.session.add(comment)
        db.session.add(user)
        db.session.commit()

        return_value = {
            "message": "Upvoted successfully",
            "comment_id": comment_id,
            "comment_upvotes":  comment.upvotes,
            "comment_downvotes":  comment.downvotes,
            "status": 200,
        }

        return jsonify(return_value)

    elif (action_type == "downvote"):

        if(comment_id in user_downvotes):
            raise BusinessValidationError(
                status_code=400, error_message="Already downvoted")

        if(comment_id in user_upvotes):
            user_upvotes = user_upvotes.replace(comment_id, "")
            user_upvotes += "," + user_upvotes

            user.upvotes = user_upvotes
            comment.upvotes -= 1

        user_downvotes += "," + comment_id
        user.downvotes = user_downvotes
        comment.downvotes = comment.downvotes + 1

        db.session.add(comment)
        db.session.add(user)
        db.session.commit()

        return_value = {
            "message": "Downvoted successfully",
            "comment_id": comment_id,
            "comment_upvotes":  comment.upvotes,
            "comment_downvotes":  comment.downvotes,
            "status": 200,
        }

        return jsonify(return_value)

    else:
        raise BusinessValidationError(
            status_code=400, error_message="Invalid action type")
