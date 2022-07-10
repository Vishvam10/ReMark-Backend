from application.utils.validation import BusinessValidationError
from application.models import Annotation, User
from application.database import db

from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask import jsonify, request

import uuid


user_output_fields = {
    "user_id": fields.String,
    "username": fields.String,
    "email_id": fields.String,
    "webhook_url": fields.String,
    "app_preferences": fields.String,
}