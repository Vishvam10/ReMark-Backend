import uuid

from application.models.Annotation import Annotation
from application.models.User import User
from application.models.Website import Website

from application.utils.validation import BusinessValidationError
from application.utils.hash import generate_random_id

from application.database import db

from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask import jsonify, request

from flask import current_app as app

website_output_fields = {
    "website_id" : fields.String,
    "website_url" : fields.String,
    "n_annotations" : fields.Integer,
    "annotation_limit" : fields.Integer,

    "admin" : fields.String,
    "admin_type" : fields.String,
}

class WebsiteAPI(Resource):
    @marshal_with(website_output_fields)
    def get(self, website_id) :
        website = db.session.query(Website).filter(Website.website_id == website_id).first()
        if website is None :
            raise BusinessValidationError(status_code=400, error_message="No such website ID exists")

        return website

    def post(self):
        data = request.json
        website_url = data["website_url"]
        n_annotations = 0

        admin = data["admin_user_id"]
        admin_type = data["admin_type"]

        if website_url is None or website_url == "":
            raise BusinessValidationError(
                status_code=400, error_message="Website URL is required")
        if admin is None or admin == "":
            raise BusinessValidationError(
                status_code=400, error_message="Admin user ID is required")
        if admin_type is None or admin_type == "":
            raise BusinessValidationError(
                status_code=400, error_message="Admin type is required")

        if(admin_type == "BASIC") :
            annotation_limit = 1000
        elif(admin_type == "PRO") :
            annotation_limit = 10000
        else :
            raise BusinessValidationError(status_code=400, error_message="Invalid admin type")

        website_id = generate_random_id()

        new_website = Website(website_id=website_id, website_url=website_url, n_annotations=n_annotations, annotation_limit=annotation_limit, admin=admin, admin_type=admin_type)

        db.session.add(new_website)
        db.session.commit()

        return_value = {
            "message": "New Website Created",
            "status": 201,
            "data" : {
                "website_url": website_url,
                "website_id": website_id,
                "admin" : admin,
                "admin_type" : admin_type
            }
        }

        return jsonify(return_value)


@app.route('/api/website/all', methods=["GET"])
def get_all_websites() :
    websites = db.session.query(Website).all()
    return jsonify(websites)

