from application.models.UserPreference import UserPreference
from application.utils.validation import BusinessValidationError
from application.utils.hash import check_hashed_password, check_hashed_password, create_hashed_password, generate_random_id, generate_api_key
from application.utils.check_headers import check_headers
from application.database.database import db

from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import jsonify, request

from flask import current_app as app
from flask import Blueprint

from application.models.User import User
from application.models.Token import Token
from application.models.Annotation import Annotation
from application.models.Comment import Comment
from application.models.Website import Website

allowed_authorities = ["admin", "user"]

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
    def get(self, user_id):
        user = db.session.query(User).filter(User.user_id == user_id).first()
        return user

    def post(self):
        ID = generate_random_id()
        data = request.json
        email_id = data["email_id"]
        username = data["username"]
        password = data["password"]
        bio = data["bio"]
        authority = data["authority"]

        if email_id is None or email_id == "":
            raise BusinessValidationError(
                status_code=400, error_message="Email ID is required")
        if username is None or username == "":
            raise BusinessValidationError(
                status_code=400, error_message="Username is required")
        if password is None or password == "":
            raise BusinessValidationError(
                status_code=400, error_message="Password is required")

        if authority not in allowed_authorities:
            raise BusinessValidationError(
                status_code=400, error_message="Authority is incorrectly specified")

        hashed_password = create_hashed_password(password)

        user = db.session.query(User).filter(User.username == username).first()

        if user:
            raise BusinessValidationError(
                status_code=400, error_message="Duplicate user")

        email_check = db.session.query(User).filter(
            User.email_id == email_id).first()
        username_check = db.session.query(User).filter(
            User.username == username).first()

        if email_check:
            raise BusinessValidationError(
                status_code=400, error_message="Email already in use")
        if username_check:
            raise BusinessValidationError(
                status_code=400, error_message="Username in use")

        new_user = User(user_id=ID, username=username, password=hashed_password,
                        email_id=email_id, authority=authority, bio=bio)

        db.session.add(new_user)

        if authority == "admin":

            # Create API_KEY for the admin - This
            # is common across all the websites that
            # the admin creates
            token = db.session.query(Token).filter(Token.user_id == ID).first()

            if token:
                raise BusinessValidationError(
                    status_code=400, error_message="Token already exists")

            api_key = generate_api_key(32)
            new_token = Token(user_id=ID, api_key=api_key)
            db.session.add(new_token)

            pref = db.session.query(UserPreference).filter(UserPreference.user_id == ID).first()

            if pref is None:
                new_pref = UserPreference(user_id=ID, show_moderated_comments=True, comments_limit_per_annotation=10, default_theme="light", brand_colors = "")
                db.session.add(new_pref)


        db.session.commit()

        return_value = {
            "message": f'New {authority} created',
            "status": 201,
            "data": {
                "user_id": ID,
                "user_name": username
            }
        }

        return jsonify(return_value)

    @jwt_required()
    @marshal_with(user_output_fields)
    def put(self, user_id):
        check_headers(request=request)
        data = request.json
        username = data["username"]
        email_id = data["email_id"]
        bio = data["bio"]

        if(not user_id or not username or not email_id):
            raise BusinessValidationError(
                status_code=400, error_message="One or more fields are missing")

        user = db.session.query(User).filter(User.user_id == user_id).first()

        if(user is None):
            raise BusinessValidationError(
                status_code=400, error_message="Invalid user ID or no such user exists")

        user_list = db.session.query(User).all()

        for u in user_list:
            ud = u.__dict__
            if(user.username != username and ud["username"] == username):
                raise BusinessValidationError(
                    status_code=400, error_message="Username already exists")
            if(user.email_id != email_id and ud["email_id"] == email_id):
                raise BusinessValidationError(
                    status_code=400, error_message="Email ID already exists")

        user.username = username
        user.email_id = email_id
        user.bio = bio

        db.session.add(user)
        db.session.commit()
        return user

    @jwt_required()
    def delete(self, user_id):
        check_headers(request=request)
        user = db.session.query(User).filter(User.user_id == user_id).first()

        if(user is None):
            raise BusinessValidationError(
                status_code=400, error_message="Invalid user ID or no such user exists")

        authority = user.__dict__["authority"]

        if(authority == "admin"):

            # 1. Delete all the comments of annotations
            annotations = db.session.query(Annotation).filter(
                Annotation.created_by == user_id).all()

            # The website_id is common for all annotations belonging to a
            # particular website, so we can pick it up any one the annotations
            if(len(annotations) != 0):
                website_id = annotations[0].__dict__["website_id"]
                if(website_id):
                    for annotation in annotations:
                        annotation_id = annotation.__dict__["annotation_id"]
                        db.session.query(Comment).where(
                            Comment.annotation_id == annotation_id).delete(synchronize_session=False)

                # 2. Delete the annotations
                db.session.query(Annotation).where(
                    Annotation.created_by == user_id).delete(synchronize_session=False)

                # 3. Delete the registered website
                db.session.query(Website).where(
                    Website.website_id == website_id).delete(synchronize_session=False)

            # 4. Delete the API_KEY
            db.session.query(Token).where(
                Token.user_id == user_id).delete(synchronize_session=False)

            # 5. Delete the user
            db.session.query(User).where(User.user_id == user_id).delete(
                synchronize_session=False)

            db.session.commit()

            return_value = {
                "message": "Admin deleted successfully",
                "status": 200,
            }

            return jsonify(return_value)

        if(authority == "user"):

            # 1. Delete all the comments
            db.session.query(Comment).where(
                Comment.created_by == user_id).delete(synchronize_session=False)

            # 2. Delete the user
            db.session.query(User).where(User.user_id == user_id).delete(
                synchronize_session=False)

            db.session.commit()

            return_value = {
                "message": "User deleted successfully",
                "status": 200,
            }

            return jsonify(return_value)

        return_value = {
            "message": "Some error occured",
            "status": 500,
        }
        return jsonify(return_value)


@app.route('/api/user/all_users', methods=["GET"])
def get_all_users():
    users = db.session.query(User).all()
    # jsonify() works because the @dataclass
    # decorator is present in the User model
    return jsonify(users)


@app.route('/api/user/update_user_preferences/<string:user_id>', methods=["GET", "PUT"])
def user_preferences(user_id):
    if(request.method == "GET"):
        user = db.session.query(User).filter(User.user_id == user_id).first()
        if(user is None):
            raise BusinessValidationError(
                status_code=400, error_message="Invalid user ID or no such user exists")

        data = {
            "webhook_url": user.webhook_url,
            "user_preferences": user.user_preferences
        }
        return jsonify(data)

    if(request.method == "PUT"):
        data = request.json
        webhook_url = data["webhook_url"]
        user_preferences = data["user_preferences"]

        user = db.session.query(User).filter(User.user_id == user_id).first()

        if(user is None):
            raise BusinessValidationError(
                status_code=400, error_message="Invalid user ID or no such user exists")

        user.webhook_url = webhook_url
        user.user_preferences = user_preferences

        db.session.add(user)
        db.session.commit()

        return_value = {
            "message": "Updated user preferences"
        }

        return jsonify(return_value)


@jwt_required()
@app.route('/api/update_password/<string:user_id>', methods=["POST"])
def update_password(user_id):
    check_headers(request=request)
    data = request.json
    current_password = data["current_password"]
    new_password = data["new_password"]

    if current_password is None or current_password == "":
        raise BusinessValidationError(
            status_code=400, error_message="Current Password is required")
    if new_password is None or new_password == "":
        raise BusinessValidationError(
            status_code=400, error_message="New Password is required")

    user = db.session.query(User).filter(User.user_id == user_id).first()

    if user is None:
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
    }

    return jsonify(return_value)
