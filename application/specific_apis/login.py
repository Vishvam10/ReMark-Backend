from flask import request
from application.database.database import db
from flask_jwt_extended import create_access_token
from flask import current_app as app
import bcrypt

from flask import jsonify, request

from application.models.User import User

from application.utils.validation import BusinessValidationError


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]
    authority = data["authority"]
    user = db.session.query(User).filter(User.username == username).first()

    if(user is None):
        raise BusinessValidationError(
            status_code=400, error_message="Invalid username or no such user exists")

    if(user.__dict__["authority"] != authority):
        raise BusinessValidationError(
            status_code=400, error_message="Invalid authority")

    if(password == "" or password is None):
        raise BusinessValidationError(
            status_code=400, error_message="Incorrect Password")
    else:
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
        "user_name": username,
        "access_token": access_token,
        "user_authority": user.authority
    }
    return jsonify(return_value)
