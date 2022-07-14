from requests import delete
from application.utils.validation import BusinessValidationError
from application.utils.hash import generate_api_key

from application.database import db

from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask import jsonify, request

from flask import current_app as app

from application.models.User import User
from application.models.Token import Token


token_output_fields = {
    "user_id": fields.String,
    "api_key": fields.String,
}

class TokenAPI(Resource):
    @marshal_with(token_output_fields)
    def get(self, user_id) :
        user = db.session.query(User).filter(User.user_id == user_id).first()
        if user is None :
            raise BusinessValidationError(status_code=400, error_message="Invalid User ID")
        
        token = db.session.query(Token).filter(Token.user_id == user_id)

        if token is None :
            raise BusinessValidationError(status_code=400, error_message="Token does not exist")

        return_value = {
            "status": 200,
            "data" : {
                "user_id": user_id,
                "api_key": token,
            }
        }

        return jsonify(return_value)

    def post(self, user_id):
        user = db.session.query(User).filter(User.user_id == user_id)
        
        if user is None :
            raise BusinessValidationError(status_code=400, error_message="Invalid User ID")


        api_key = generate_api_key(32)

        new_token = Token(user_id=user_id, api_key=api_key)

        db.session.add(new_token)
        db.session.commit()

        return_value = {
            "message": "New Token Created",
            "status": 201,
            "data" : {
                "user_id": user_id,
                "api_key": api_key,
            }
        }

        return jsonify(return_value)
        

    # @marshal_with(token_output_fields)
    # def put(self, user_id) :
     
    def delete(self, user_id) :
        user = db.session.query(User).filter(User.user_id == user_id)
        
        if user is None :
            raise BusinessValidationError(status_code=400, error_message="Invalid User ID")

          
        token = db.session.query(Token).filter(Token.user_id == user_id)

        if token is None :
            raise BusinessValidationError(status_code=400, error_message="Token does not exist")

        db.session.query(Token).filter(Token.user_id == user_id).delete(synchronize_session=False)
        db.session.commit()

        return_value = {
            "message": "Token deleted succesfully",
            "status": 200,
            "data" : {
                "user_id": user_id,
                "deleted_api_key" : token
            }
        }

        return jsonify(return_value)