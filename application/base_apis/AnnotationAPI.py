import uuid

from application.models.Annotation import Annotation
from application.models.Comment import Comment
from application.models.Website import Website

from application.utils.validation import BusinessValidationError
from application.utils.check_headers import check_headers

from application.database.database import db

from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import jsonify, request

from flask import current_app as app

comment_output_fields = {
    'comment_id': fields.String,
    'created_by': fields.String,
    'created_at': fields.String,
    'updated_at': fields.String,
    'content_html': fields.String,
    'upvoted': fields.Integer,
    'downvotes': fields.Integer,
    'mod_required': fields.String
}

annotation_output_fields = {
    "annotation_id": fields.String,
    "annotation_name": fields.String,

    "website_id": fields.String,
    "website_uri": fields.String,

    "tags": fields.String,
    "node_xpath": fields.String,

    "resolved": fields.Boolean,

    "created_at": fields.DateTime,
    "updated_at": fields.DateTime,
    "created_by_id": fields.String,
    "created_by": fields.String,
    "modified_by_id": fields.String,
    "modified_by": fields.String,

    "comments": fields.List(fields.Nested(comment_output_fields))
}


class AnnotationAPI(Resource):
    @jwt_required()
    @marshal_with(annotation_output_fields)
    def get(self, annotation_id):
        check_headers(request=request)

        annotation = db.session.query(Annotation).filter(
            Annotation.annotation_id == annotation_id).first()
        if(annotation is None):
            raise BusinessValidationError(
                status_code=400, error_message="Invalid annotation ID")
        return annotation

    @jwt_required()
    def post(self):
        check_headers(request=request)

        annotation_id = str(uuid.uuid4()).replace("-", "")

        data = request.json

        annotation_name = data["annotation_name"]
        website_id = data["website_id"]
        website_uri = data["website_uri"]
        user_id = data["user_id"]
        user_name = data["user_name"]

        node_xpath = data["node_xpath"]
        html_id = data["html_id"]
        html_tag = data["html_tag"]
        html_text_content = data["html_text_content"]

        tags = data["tags"]
        resolved = False

        website = db.session.query(Website).filter(
            Website.website_id == website_id).first()
        if website is None:
            raise BusinessValidationError(
                status_code=400, error_message="No such website ID exists")

        n_annotations = website.__dict__["n_annotations"]
        annotation_limit = website.__dict__["annotation_limit"]

        if(n_annotations + 1 > annotation_limit):
            raise BusinessValidationError(
                status_code=400, error_message="Annotation limit exceeded")

        if user_id is None or user_id == "":
            raise BusinessValidationError(
                status_code=400, error_message="User ID is required")
        if user_name is None or user_name == "":
            raise BusinessValidationError(
                status_code=400, error_message="Username is required")
        if annotation_name is None or annotation_name == "":
            raise BusinessValidationError(
                status_code=400, error_message="Content is required")
        if node_xpath is None or node_xpath == "":
            raise BusinessValidationError(
                status_code=400, error_message="HTML node data tag is required")
        if html_tag is None or html_tag == "":
            raise BusinessValidationError(
                status_code=400, error_message="HTML tag is required")

        # 1. Add the annotation
        new_annotation = Annotation(annotation_id=annotation_id, annotation_name=annotation_name, website_id=website_id, website_uri=website_uri, node_xpath=node_xpath,
                                    tags=tags, html_id=html_id, html_tag=html_tag, html_text_content=html_text_content, resolved=resolved, created_by=user_name, created_by_id=user_id)

        db.session.add(new_annotation)

        # 2. Update n_annotations for that website_id
        website.n_annotations = (n_annotations + 1)
        db.session.add(website)

        db.session.commit()

        return_value = {
            "message": "New Annotation Created",
            "status": 201,
            "data": {
                "created_by": user_name,
                "created_by_id": user_id,
                "annotation_id": annotation_id,
                "annotation_name": annotation_name,
                "node_xpath": node_xpath,
                "n_annotations": (n_annotations + 1)
            }
        }

        return jsonify(return_value)

    @jwt_required()
    def put(self, annotation_id):
        check_headers(request=request)
    
        data = request.json
        action_type = data["action_type"].split(",")
        annotation = db.session.query(Annotation).filter(
            Annotation.annotation_id == annotation_id).first()

        message = "Annotation edited successfully !"
        if(len(action_type) > 3):
            raise BusinessValidationError(
                status_code=400, error_message="Invalid action types")

        if annotation is None:
            raise BusinessValidationError(
                status_code=400, error_message="Invalid annotation ID")

        if("edit_name" in action_type or "edit_tags" in action_type or "edit_resolved" in action_type):

            if("edit_name" in action_type):
                new_name = data["new_name"]

                if new_name is None or new_name == "":
                    raise BusinessValidationError(
                        status_code=400, error_message="Annotation name can not be empty")

                annotation.annotation_name = new_name

            if("edit_tags" in action_type):
                new_tags = data["new_tags"]
                annotation.tags = new_tags

            if("edit_resolved" in action_type):
                if(annotation.resolved == True):
                    message = "Annotation unresolved successfully !"
                    annotation.resolved = False
                    db.session.add(annotation)
                    db.session.commit()
                elif(annotation.resolved == False):
                    message = "Annotation resolved successfully !"
                    annotation.resolved = True
                else:
                    raise BusinessValidationError(
                        status_code=400, error_message="Invalid value for boolean variable : resolved")
            
            db.session.add(annotation)
            db.session.commit()

            return_value = {
                "message": message,
                "status": 201,
            }

            return jsonify(return_value)

        else:
            raise BusinessValidationError(
                status_code=400, error_message="Invalid action type")

    @jwt_required()
    def delete(self, annotation_id):
        check_headers(request=request)

        annotation = db.session.query(Annotation).filter(
            Annotation.annotation_id == annotation_id).first()
        if(annotation is None):
            raise BusinessValidationError(
                status_code=400, error_message="Invalid annotation ID")

        website_id = annotation.__dict__["website_id"]

        # 1. Delete all the comments
        db.session.query(Comment).where(Comment.annotation_id ==
                                        annotation_id).delete(synchronize_session=False)

        # 2. Delete the annotations
        db.session.query(Annotation).filter(
            Annotation.annotation_id == annotation_id).delete(synchronize_session=False)

        # 3. Decrease n_annotations for that website_id
        website = db.session.query(Website).filter(
            Website.website_id == website_id).first()
        if website is None:
            raise BusinessValidationError(
                status_code=400, error_message="No such website ID exists")

        n_annotations = website.__dict__["n_annotations"] - 1
        website.n_annotations = n_annotations

        db.session.add(website)

        db.session.commit()

        return_value = {
            "annotation_id": annotation_id,
            "message": "Annotation deleted successfully",
            "status": 200,
        }

        return jsonify(return_value)


@jwt_required()
@app.route('/api/annotation/all/<string:website_id>', methods=["GET"])
def get_all_annotations_by_website_id(website_id):
    check_headers(request=request)

    website = db.session.query(Website).filter(
        Website.website_id == website_id).first()
    if(website is None):
        raise BusinessValidationError(
            status_code=400, error_message="Invalid website ID")

    annotations = db.session.query(Annotation).filter(
        Annotation.website_id == website_id).all()

    return jsonify(annotations)
