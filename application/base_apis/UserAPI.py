import uuid

from application.utils.validation import BusinessValidationError
from application.utils.hash import check_hashed_password, check_hashed_password, create_hashed_password

from application.database import db

from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask import jsonify, request

from flask import current_app as app

from application.models.User import User


user_output_fields = {
    "user_id": fields.String,
    "username": fields.String,
    "email_id": fields.String,
    "authority": fields.String,
    "bio": fields.String,
    "created_at": fields.String,
    "modified_at": fields.String,
}

class UserAPI(Resource):
    @marshal_with(user_output_fields)
    def get(self, user_id) :
        user = db.session.query(User).filter(User.user_id == user_id).first()
        return user

    def post(self):
        ID = str(uuid.uuid4()).replace("-", "")
        data = request.json
        email_id = data["email_id"]
        username = data["username"]
        password = data["password"]
        bio = data["bio"]
        authority = data["authority"]
        api_key = data['api_key']

        if email_id is None or email_id == "":
            raise BusinessValidationError(
                status_code=400, error_message="Email ID is required")
        if username is None or username == "":
            raise BusinessValidationError(
                status_code=400, error_message="Username is required")
        if password is None or password == "":
            raise BusinessValidationError(
                status_code=400, error_message="Password is required")
    
        if api_key is None or api_key == "" :
            if authority != "user" or authority == "" :
                raise BusinessValidationError(
                    status_code=400, error_message="Authority is incorrectly specified")
        else :
            if authority != "admin" or authority == "" :
                raise BusinessValidationError(status_code=400, error_message="Authority is incorrectly specified")


        hashed_password = create_hashed_password(password)

        user = db.session.query(User).filter(User.username == username).first()
        
        if user:
            raise BusinessValidationError(
                status_code=400, error_message="Duplicate user")

        new_user = User(user_id=ID, username=username, password=hashed_password, email_id=email_id, authority=authority, api_key=api_key, bio=bio)

        db.session.add(new_user)
        db.session.commit()

        return_value = {
            "message": "New User Created",
            "status": 201,
            "data" : {
                "user_id": ID,
                "user_name": username,
            }
        }

        return jsonify(return_value)

    @marshal_with(user_output_fields)
    def put(self, user_id) :
        data = request.json
        username = data["username"]
        email_id = data["email_id"]
        bio = data["bio"]

        if(not user_id or not username or not email_id) :
            raise BusinessValidationError(status_code=400, error_message="One or more fields are missing")

        user = db.session.query(User).filter(User.user_id == user_id).first()
        
        if(user is None):
            raise BusinessValidationError(status_code=400, error_message="Invalid user ID or no such user exists")

        user_list = db.session.query(User).all()
        
        for u in user_list :
            ud = u.__dict__
            if(user.username != username and ud["username"] == username) :
                raise BusinessValidationError(status_code=400, error_message="Username already exists")
            if(user.email_id != email_id and ud["email_id"] == email_id) :
                raise BusinessValidationError(status_code=400, error_message="Email ID already exists")

        user.username = username
        user.email_id = email_id
        user.bio = bio

        db.session.add(user)
        db.session.commit()
        return user

    def delete(self, user_id) :
        # 1. Delete all data

        # 2. Delete the user
        # db.session.query(User).filter(User.user_id == user_id).delete(synchronize_session=False)
        # db.session.commit()

        return_value = {
            "user_id": user_id,
            "message": "User deleted succesfully",
            "status": 200,
        }

        return jsonify(return_value)


@app.route('/api/user/all', methods=["GET"])
def get_all_users() :
    users = db.session.query(User).all()
    # data = []
    # for u in users : 
    #     data.append(
    #         # {
    #         #     "user_id": u.__dict__["user_id"], 
    #         #     "username" : u.__dict__["username"],
    #         #     "email_id": u.__dict__["email_id"]
    #         # }
    #         json.u.__dict__
    #     )
    # return_value = {
    #     "data" : data
    # }
    return jsonify(users)

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

