from flask import request
from application.database.dev.database import db
from flask import current_app as app

from flask import jsonify, request, send_file
from flask_jwt_extended import jwt_required

from application.models.User import User
from application.utils.validation import BusinessValidationError

media = app.config["MEDIA_FOLDER"]

@app.route("/api/download/<string:user_id>", methods=["GET"])
@jwt_required()
def download_file(user_id):
    user = db.session.query(User).filter(User.user_id == user_id).first()
    if(user.__dict__["authority"] != "admin") :
        raise BusinessValidationError(
            status_code=400, error_message="Only admins can download this file !")
    
    file_type = "js"
    f = media + "\\" + "remark.v.0.1" + "." + file_type

    return send_file(f, mimetype='text/javascript', attachment_filename="remark.v.0.1.js", as_attachment=True)
