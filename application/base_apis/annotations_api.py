from application.utils.validation import BusinessValidationError
from application.models import Annotation, User
from application.database import db

from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask import jsonify, request

import uuid


user_output_fields = {
    "user_id": fields.String,
    "username": fields.String,
    "email_id": fields.String,
    "webhook_url": fields.String,
    "app_preferences": fields.String,
}

# _ User API


class AnnotationAPI(Resource):
    @marshal_with(user_output_fields)
    def get(self, user_id) :
        annotations = db.session.query(User).filter(User.user_id == user_id).first()
        return annotations

    def post(self):
        ID = str(uuid.uuid4()).replace("-", "")
        data = request.json
        username = data["username"]
        password = data["password"]
        email = data["email"]
        webhook_url = ""
        app_preferences = ""

        if username is None or username == "":
            raise BusinessValidationError(
                status_code=400, error_message="Username is required")
        if password is None or password == "":
            raise BusinessValidationError(
                status_code=400, error_message="Password is required")
        if email is None or email == "":
            raise BusinessValidationError(
                status_code=400, error_message="Email ID is required")
    
        hashed_password = createHashedPassword(password)

        user = db.session.query(User).filter(User.username == username).first()
        
        if user:
            raise BusinessValidationError(
                status_code=400, error_message="Duplicate user")

        new_user = User(user_id=ID, username=username,
                        password=hashed_password, email_id=email, phone_no=phone, webhook_url=webhook_url, app_preferences=app_preferences)
        db.session.add(new_user)
        db.session.commit()

        return_value = {
            "message": "New User Created",
            "status": 200,
            "user_id": ID,
            "user_name": username,
        }

        return jsonify(return_value)

    @marshal_with(user_output_fields)
    def put(self, user_id) :
        data = request.json
        username = data["user_name"]
        email_id = data["email_id"]

        if(not user_id or not username or not email_id) :
            raise BusinessValidationError(status_code=400, error_message="One or more fields are missing")

        user = db.session.query(User).filter(User.user_id == user_id).first()
        
        if(user is None):
            raise BusinessValidationError(status_code=400, error_message="Invalid user ID or no such user exists")

        user_list = db.session.query(User).all()
        
        for u in user_list :
            ud = u.__dict__
            print("********** USER **********", ud)
            if(user.username != username and ud["username"] == username) :
                raise BusinessValidationError(status_code=400, error_message="Username already exists")
            if(user.email_id != email_id and ud["email_id"] == email_id) :
                raise BusinessValidationError(status_code=400, error_message="Email ID already exists")

        user.username = username
        user.email_id = email_id

        db.session.add(user)
        db.session.commit()
        return user

    def delete(self, user_id) :
        # 1. Delete all data

        # 2. Delete the user
        db.session.query(User).filter(User.user_id == user_id).delete(synchronize_session=False)
        db.session.commit()

        return_value = {
            "user_id": user_id,
            "message": "User deleted succesfully",
            "status": 200,
        }

        return jsonify(return_value)

