from flask import request
from application.models import *
from application.database import db
from flask_jwt_extended import create_access_token
from flask import current_app as app
import bcrypt

from flask import jsonify, request

from application.models.User import User

from application.utils.validation import BusinessValidationError
from application.utils.check_headers import check_headers

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    authority = data["authority"]
    if(authority == "user") :
        check_headers(request=request)
    
    username = data["username"]
    password = data["password"]
    user = db.session.query(User).filter(User.username == username).first()

    if(user is None):
        raise BusinessValidationError(
            status_code=400, error_message="Invalid username or no such user exists")

    if(password != ""):
        hashed_password = user.password
        string_password = hashed_password.decode('utf8')
        if(not bcrypt.checkpw(password.encode('utf8'), string_password.encode('utf8'))):
            raise BusinessValidationError(
                status_code=400, error_message="Incorrect Password")

    access_token = create_access_token(identity=username)

    return_value = {
        "message": "Logged in successfully",
        "status": 200,
        "user_id": user.user_id,
        "user_name" : username,
        "access_token": access_token,
        "user_authority" : user.authority
    }
    return jsonify(return_value)