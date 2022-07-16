from application.utils.validation import BusinessValidationError

from application.database import db

from application.models.Token import Token

def check_headers(request) :
    if(request.headers['API_KEY'] is None or request.headers['API_KEY'] == "") :
        raise BusinessValidationError(status_code=400, error_message="Request header 'API_KEY' missing")
    
    api_key = request.headers['API_KEY']

    ak = db.session.query(Token).filter(Token.api_key == api_key).first()

    # (FUTURE) Logs these requests in a logfile or a table in DB

    if(ak is None) :
        raise BusinessValidationError(status_code=400, error_message="Invalid API_KEY")
    
    return True

