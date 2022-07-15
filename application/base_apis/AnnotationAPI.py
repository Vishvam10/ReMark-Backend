import uuid
from venv import create

from application.models.Annotation import Annotation
from application.models.User import User
from application.models.Website import Website

from application.utils.validation import BusinessValidationError

from application.database import db

from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask import jsonify, request

from flask import current_app as app

annotation_output_fields = {
    "annotation_id" : fields.String,
    "website_id" : fields.String,
    "website_uri" : fields.String,

    "content" : fields.String,
    "html_content" : fields.String,

    "parent_node" : fields.String,

    "tags" : fields.String,
    "upvotes" : fields.Integer,
    "downvotes" : fields.Integer,
    "mod_required" : fields.Boolean,

    "resolved" : fields.Boolean,

    "created_at" : fields.DateTime,
    "modified_at" : fields.DateTime, 
    "created_by" : fields.String,
    "modified_by" : fields.String,
}

class AnnotationAPI(Resource):
    @marshal_with(annotation_output_fields)
    def get(self, annotation_id) :
        annotation = db.session.query(Annotation).filter(Annotation.annotation_id == annotation_id).first()
        if(annotation is None) :
            raise BusinessValidationError(status_code=400, error_message="Invalid annotation ID")
        return annotation

    def post(self):
        annotation_id = str(uuid.uuid4()).replace("-", "")
        
        data = request.json
        
        annotation_name = data["annotation_name"]
        website_id = data["website_id"]
        website_uri = data["website_uri"]
        created_by = data["user_id"]
        html_node_data_tag = data["html_node_data_tag"]

        tags = data["tags"]
        resolved = False

        if created_by is None or created_by == "":
            raise BusinessValidationError(
                status_code=400, error_message="User ID is required")
        if annotation_name is None or annotation_name == "":
            raise BusinessValidationError(
                status_code=400, error_message="Content is required")
        if html_node_data_tag is None or html_node_data_tag == "":
            raise BusinessValidationError(
                status_code=400, error_message="HTML node data tag is required")

        new_annotation = Annotation(annotation_id=annotation_id, annotation_name=annotation_name, website_id=website_id, website_uri=website_uri, html_node_data_tag=html_node_data_tag, tags=tags, resolved=resolved, created_by=created_by)

        db.session.add(new_annotation)
        db.session.commit()

        return_value = {
            "message": "New Annotation Created",
            "status": 201,
            "data" : {
                "created_by": created_by,
                "annotation_id": annotation_id,
                "annotation_name" : annotation_name,
                "html_node_data_tag" : html_node_data_tag,
                "created_by" : created_by
            }
        }

        return jsonify(return_value)

    @marshal_with(annotation_output_fields)
    def put(self, annotation_id) :
        data = request.json

        user_id = data["user_id"]
        content = data["content"]
        html_content = data["html_content"]
        tags = data["tags"]

        if user_id is None or user_id == "":
            raise BusinessValidationError(
                status_code=400, error_message="User ID is required")
        if content is None or content == "":
            raise BusinessValidationError(
                status_code=400, error_message="Content is required")
        if html_content is None or html_content == "":
            raise BusinessValidationError(
                status_code=400, error_message="HTML content is required")

        annotation = db.session.query(Annotation).filter(Annotation.annotation_id == annotation_id).first()
        user = db.session.query(User).filter(User.user_id == user_id).first()
        
        if(annotation is None):
            raise BusinessValidationError(status_code=400, error_message="Invalid annotation ID or no such annotation exists")
        if(user is None):
            raise BusinessValidationError(status_code=400, error_message="Invalid annotation ID or no such annotation exists")

        annotation.content = content
        annotation.html_content = html_content
        annotation.tags = tags
        annotation.modified_by = user_id

        db.session.add(annotation)
        db.session.commit()
        return annotation

    def delete(self, annotation_id) :
        # 1. Delete all replies

        # 2. Delete the annotation
        # db.session.query(Annotation).filter(Annotation.annotation_id == annotation_id).delete(synchronize_session=False)
        # db.session.commit()

        return_value = {
            "annotation_id": annotation_id,
            "message": "Annotation deleted successfully",
            "status": 200,
        }

        return jsonify(return_value)


@app.route('/api/annotation/all', methods=["GET"])
def get_all_annotations() :
    annotations = db.session.query(User).all()
    data = []
    for u in annotations : 
        data.append(
            {
                "annotation_id": u.__dict__["annotation_id"], 
                "content" : u.__dict__["content"],
                "html_content": u.__dict__["html_content"],
                "parent_node": u.__dict__["parent_node"],
                "tags": u.__dict__["tags"],
                "upvotes": u.__dict__["upvotes"],
                "downvotes": u.__dict__["downvotes"],
                "resolved": u.__dict__["resolved"],
                "mod_req": u.__dict__["mod_req"],
            }
        )
    return_value = {
        "data" : data
    }
    return jsonify(return_value)