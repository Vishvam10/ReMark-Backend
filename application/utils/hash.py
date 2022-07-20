import string
import random
import bcrypt
import uuid
import secrets

from application.utils.validation import BusinessValidationError

def create_hashed_password(password) :
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

def check_hashed_password(password, hashed_password) :
    return bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8'))

def generate_api_key(length):
    if(length < 16) :
        raise BusinessValidationError(status_code=400, error_message="Insufficient length")
    
    api_key = secrets.token_urlsafe(length)                                 
    return api_key

def generate_random_id() :
    return str(uuid.uuid4()).replace("-", "")