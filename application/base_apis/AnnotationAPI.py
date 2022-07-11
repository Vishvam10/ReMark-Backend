from __future__ import annotations
import uuid

from pyparsing import html_comment
from application.models.Annotation import Annotation
from application.models.User import User

from application.utils.validation import BusinessValidationError
from application.utils.hash import check_hashed_password, check_hashed_password, create_hashed_password

from application.database import db

from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask import jsonify, request

from flask import current_app as app

from application.models.Annotation import *


annotation_output_fields = {
    "annotation_id" : fields.String,
    "website_id" : fields.String,

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
    def get(self, website_id) :
        annotation = db.session.query(Annotation).filter(Annotation.website_id == website_id).first()
        return annotation

    def post(self):
        annotation_id = str(uuid.uuid4()).replace("-", "")
        website_id = str(uuid.uuid4()).replace("-", "")
        data = request.json
        
        created_by = data["user_id"]

        content = data["content"]
        html_content = data["html_content"]
        parent_node = data["parent_node"]

        tags = data["tags"]
        upvotes = 0
        downvotes = 0
        mod_required = False
        resolved = False



        if created_by is None or created_by == "":
            raise BusinessValidationError(
                status_code=400, error_message="User ID is required")
        if content is None or content == "":
            raise BusinessValidationError(
                status_code=400, error_message="Content is required")
        if html_comment is None or html_comment == "":
            raise BusinessValidationError(
                status_code=400, error_message="HTML content is required")


        new_annotation = Annotation(annotation_id=annotation_id, website_id=website_id,content=content, html_content=html_content, parent_node=parent_node, tags=tags, upvotes=upvotes, downvotes=downvotes, mod_required=mod_required, resolved=resolved)

        db.session.add(new_annotation)
        db.session.commit()

        return_value = {
            "message": "New Annotation Created",
            "status": 201,
            "data" : {
                "created_by": created_by,
                "content": content,
                "html_content" : html_content,
                "website_id" : website_id
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
        if html_comment is None or html_comment == "":
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
            "message": "Annotation deleted succesfully",
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

@app.route('/api/user/update_user_preferences/<string:user_id>', methods=["GET","PUT"])
def user_preferences(user_id) :
    if(request.method == "GET") :
        user = db.session.query(User).filter(User.user_id == user_id).first()    
        if(user is None):
            raise BusinessValidationError(status_code=400, error_message="Invalid user ID or no such user exists")
        
        data = {
            "webhook_url" : user.webhook_url,
            "user_preferences" : user.user_preferences
        }
        return jsonify(data)

    if(request.method == "PUT") :
        data = request.json
        webhook_url = data["webhook_url"]
        user_preferences = data["user_preferences"]
        
        user = db.session.query(User).filter(User.user_id == user_id).first()
            
        if(user is None):
            raise BusinessValidationError(status_code=400, error_message="Invalid user ID or no such user exists")

        user.webhook_url = webhook_url
        user.user_preferences = user_preferences
        

        db.session.add(user)
        db.session.commit()

        return_value = {
            "message" : "Updated user preferences"
        }

        return jsonify(return_value)

@app.route('/api/password_reset/<string:user_id>', methods=["POST"])
def reset_password(user_id) :
    data = request.json
    current_password = data["current_password"]
    new_password = data["new_password"]
    
    # print("***************** OLD PASSWORD *****************", current_password)
    if current_password is None or current_password == "":
        raise BusinessValidationError(
            status_code=400, error_message="Current Password is required")
    if new_password is None or new_password == "":
        raise BusinessValidationError(
            status_code=400, error_message="New Password is required")
    
    user = db.session.query(User).filter(User.user_id == user_id).first()

    if user is None :
        raise BusinessValidationError(
            status_code=400, error_message="No such user exists")


    hashed_password = user.password
    string_password = hashed_password.decode('utf8')

    if(not check_hashed_password(current_password, string_password)):
        raise BusinessValidationError(
            status_code=400, error_message="Incorrect Password")
    
    new_hashed_password = create_hashed_password(new_password)
    user.password = new_hashed_password
    
    db.session.add(user)
    db.session.commit()

    return_value = {
        "message": "Password Changed Successfully",
        "status": 204,
        "new_password" : new_password
    }

    return jsonify(return_value)

