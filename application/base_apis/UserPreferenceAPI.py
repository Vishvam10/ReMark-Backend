from application.models.UserPreference import UserPreference
from application.utils.validation import BusinessValidationError
from application.utils.check_headers import check_headers
from application.database.dev.database import db

from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import jsonify, request


allowed_authorities = ["admin", "user"]

user_preference_output_fields = {
    "user_id": fields.String,
    "show_moderated_comments": fields.Boolean,
    "comments_limit_per_annotation": fields.Integer,
    "default_theme": fields.String,
    "brand_colors": fields.String
}


class UserPreferenceAPI(Resource):
    @jwt_required()
    @marshal_with(user_preference_output_fields)
    def get(self, user_id):
        pref = db.session.query(UserPreference).filter(UserPreference.user_id == user_id).first()
        return pref

    def post(self, user_id):
        show_moderated_comments = True
        comments_limit_per_annotation = 10
        default_theme = "light"
        brand_colors = ""

        user = db.session.query(UserPreference).filter(UserPreference.user_id == user_id).first()

        if user:
            raise BusinessValidationError(
                status_code=400, error_message="User preferences already exists")

        preference = UserPreference(user_id=user_id, show_moderated_comments=show_moderated_comments,
                        comments_limit_per_annotation=comments_limit_per_annotation, default_theme=default_theme, brand_colors=brand_colors)

        db.session.add(preference)

        db.session.commit()

        return_value = {
            "message": "Preferences created",
            "status": 201,
        }

        return jsonify(return_value)

    @jwt_required()
    @marshal_with(user_preference_output_fields)
    def put(self, user_id):
        data = request.json
        show_moderated_comments = data["show_moderated_comments"]
        comments_limit_per_annotation = int(data["comments_limit_per_annotation"])
        default_theme = data["default_theme"]
        brand_colors = data["brand_colors"]

        userPref = db.session.query(UserPreference).filter(UserPreference.user_id == user_id).first()

        if(userPref is None):
            raise BusinessValidationError(
                status_code=400, error_message="Invalid user ID or no such user exists")

        userPref.show_moderated_comments = show_moderated_comments
        userPref.comments_limit_per_annotation = comments_limit_per_annotation
        userPref.default_theme = default_theme
        userPref.brand_colors = brand_colors


        db.session.add(userPref)
        db.session.commit()
        return userPref

    @jwt_required()
    def delete(self, user_id):
        userPref = db.session.query(UserPreference).filter(UserPreference.user_id == user_id).first()

        if(userPref is None):
            raise BusinessValidationError(
                status_code=400, error_message="Invalid user ID or no such user exists")

        try : 
            db.session.query(UserPreference).where(
                UserPreference.user_id == user_id).delete(synchronize_session=False)

            db.session.commit()

            return_value = {
                "message": "User preference deleted successfully",
                "status": 200,
            }

            return jsonify(return_value)

        except :
            return_value = {
                "message": "Some error occured",
                "status": 500,
            }
            return jsonify(return_value)

