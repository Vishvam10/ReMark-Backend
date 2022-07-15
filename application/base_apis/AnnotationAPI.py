import re
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

comment_output_fields = {
    'comment_id': fields.String,
    'created_by': fields.String,
    'content': fields.String,
}

annotation_output_fields = {
    "annotation_id" : fields.String,
    "annotation_name" : fields.String,

    "website_id" : fields.String,
    "website_uri" : fields.String,

    "tags" : fields.String,
    "html_node_data_tag" : fields.String,

    "resolved" : fields.Boolean,

    "created_at" : fields.DateTime,
    "modified_at" : fields.DateTime, 
    "created_by" : fields.String,
    "modified_by" : fields.String,

    "comments" : fields.List(fields.Nested(comment_output_fields))
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
        # INDICATOR VARIABLES
        action_type = data["action_type"].split(",")
        annotation = db.session.query(Annotation).filter(Annotation.annotation_id == annotation_id).first()
        
        if(len(action_type) > 3) :
            raise BusinessValidationError(status_code=400, error_message="Invalid action types")

        if annotation is None :
            raise BusinessValidationError(status_code=400, error_message="Invalid annotation ID")
        
        if("edit_name" in action_type or "edit_tags" in action_type or "edit_resolved" in action_type) :
            

            if("edit_name" in action_type) :
                new_name = data["new_name"] 

                if new_name is None or new_name == "" :
                    raise BusinessValidationError(status_code=400, error_message="Annotation name can not be empty")

                annotation.annotation_name = new_name

            
            if("edit_tags" in action_type) :
                new_tags = data["new_tags"]
                print("********************************** NEW TAGS **********************************", new_tags)

                annotation.tags = new_tags
                db.session.add(annotation)
                db.session.commit()
            
            if("edit_resolved" in action_type) :
                new_resolved = data["new_resolved"]
                if(new_resolved == True or new_resolved == False) :
                    annotation.resolved = new_resolved
                    db.session.add(annotation)
                    db.session.commit()
                else :
                    raise BusinessValidationError(status_code=400, error_message="Invalid value for boolean variable : resolved")


        else :
            raise BusinessValidationError(status_code=400, error_message="Invalid action type")

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
def get_all_annotations_by_website_id() :
    args = request.args
    website_id = args.get("website_id")
    website = db.session.query(Website).filter(Website.website_id == website_id).first()
    if(website is None) :
        raise BusinessValidationError(status_code=400, error_message="Invalid website ID")
    
    annotations = db.session.query(Annotation).filter(Annotation.website_id == website_id).all()
    
    return jsonify(annotations)