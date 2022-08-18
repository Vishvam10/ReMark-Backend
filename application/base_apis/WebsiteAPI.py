from application.models.User import User
from application.models.Website import Website

from application.utils.validation import BusinessValidationError
from application.utils.hash import generate_random_id
from application.utils.check_headers import check_headers
from application.utils.url_operations import get_url

from application.database.dev.database import db

from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask_jwt_extended import jwt_required
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
    
    @jwt_required()
    @marshal_with(website_output_fields)
    def get(self) :
        check_headers(request=request)
        data = request.args
        if(data.get("website_id")) :
            website_id = data.get("website_id")
            website = db.session.query(Website).filter(Website.website_id == website_id).first()
            if website is None :
                raise BusinessValidationError(status_code=400, error_message="No such website ID exists")
            return website
        elif(data.get("website_url")) :
            website_url = data.get("website_url")
            website = db.session.query(Website).filter(Website.website_url == website_url).first()
            if website is None :
                raise BusinessValidationError(status_code=400, error_message="No such website URL exists")
            return website
        
        raise BusinessValidationError(status_code=400, error_message="Invalid URL arguments")
        
    @jwt_required()
    def post(self):
        check_headers(request=request)
        data = request.json
        website_url = data["website_url"]
        n_annotations = 0

        admin_id = data["admin_id"]
        admin_type = data["admin_type"]

        if website_url is None or website_url == "":
            raise BusinessValidationError(
                status_code=400, error_message="Website URL is required")
        if admin_id is None or admin_id == "":
            raise BusinessValidationError(
                status_code=400, error_message="Admin user ID is required")
        if admin_type is None or admin_type == "":
            raise BusinessValidationError(
                status_code=400, error_message="Admin type is required")

        user = db.session.query(User).filter(User.user_id == admin_id).first()

        if(user is None):
            raise BusinessValidationError(status_code=400, error_message="No such user exists")
        
        if(admin_type == "BASIC") :
            annotation_limit = 1000
        elif(admin_type == "PRO") :
            annotation_limit = 10000
        else :
            raise BusinessValidationError(status_code=400, error_message="Invalid admin type")

        website_id = generate_random_id()
        website_url = get_url(website_url)

        website = db.session.query(Website).filter(Website.website_id == website_id).first()

        if(website) :
            raise BusinessValidationError(status_code=400, error_message="Website already exists")


        new_website = Website(website_id=website_id, website_url=website_url, n_annotations=n_annotations, annotation_limit=annotation_limit, admin=admin_id, admin_type=admin_type)

        db.session.add(new_website)
        db.session.commit()

        return_value = {
            "message": "New website created",
            "status": 200,
            "data" : {
                "user_id": admin_id,
                "admin_type" : admin_type,
                "website_id": website_id
            }
        }

        return jsonify(return_value)

    @jwt_required()
    def delete(self, website_id) :
        check_headers(request=request)
        website = db.session.query(Website).filter(Website.website_id == website_id).first()
        if(website is None) : 
            raise BusinessValidationError(status_code=400, error_message="No such website ID exists")
            
        db.session.query(Website).filter(Website.website_id == website_id).delete(synchronize_session=False)
        db.session.commit()

        return_value = {
            "website_id": website_id,
            "message": "Website deleted successfully",
            "status": 200,
        }

        return jsonify(return_value)


@jwt_required() 
@app.route('/api/website/all/<string:user_id>', methods=["GET"])
def get_all_websites(user_id) :
    check_headers(request=request)

    user = db.session.query(User).filter(User.user_id == user_id).first()

    if(user is None):
        raise BusinessValidationError(status_code=400, error_message="No such user exists")

    websites = db.session.query(Website).filter(Website.admin == user_id).all()
    return jsonify(websites)
