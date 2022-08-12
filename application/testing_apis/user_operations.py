import random

from application.database.database import db
from flask_jwt_extended import create_access_token
from flask import current_app as app
from flask import jsonify, request

from application.models.User import User
from application.utils.validation import BusinessValidationError

@app.route("/api/test/user/get_random_admin", methods=["POST"])
def get_random_admin() :
    users = db.session.query(User).all()
    index = random.randint(0, len(users) - 1)
    for user in users :
        authority = user.__dic__["authority"]
        if(authority == "admin") :
            print(user)



@app.route("/api/test/user/get_random_user_id", methods=["POST"])
def get_random_admin() :
    users = db.session.query(User).all()
    for user in users :
        authority = user.__dic__["authority"]
        if(authority == "admin") :
            print(user)


