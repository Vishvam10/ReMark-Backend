from application.utils.validation import BusinessValidationError
from application.models import User
from application.utils.hash import createHashedPassword, checkHashedPassword
from application.database import db

from operator import and_
from sqlalchemy import false, true
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask import jsonify, request

from flask import current_app as app

from app import cache

import uuid


import datetime as dt

user_output_fields = {
    "user_id": fields.String,
    "username": fields.String,
    "email_id": fields.String,
    "webhook_url": fields.String,
    "app_preferences": fields.String,
}

# _ User API


class UserAPI(Resource):
    @marshal_with(user_output_fields)
    def get(self, user_id) :
        user = db.session.query(User).filter(User.user_id == user_id).first()
        return user

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


@app.route('/api/user/all', methods=["GET"])
def get_all_users() :
    users = db.session.query(User).all()
    data = []
    for u in users : 
        data.append((u.__dict__["username"], u.__dict__["user_id"]))
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

    hashed_password = user.password
    string_password = hashed_password.decode('utf8')

    # print("***************** OLD HASHED PASSWORD *****************", string_password)
    if(not checkHashedPassword(current_password, string_password)):
        raise BusinessValidationError(
            status_code=400, error_message="Incorrect Password")
    
    new_hashed_password = createHashedPassword(new_password)
    user.password = new_hashed_password
    
    # print("***************** NEW PASSWORD *****************", new_hashed_password)
    db.session.add(user)
    db.session.commit()

    return_value = {
        "message": "Password Changed Successfully",
        "status": 200,
        "new_password" : new_password
    }

    return jsonify(return_value)

