from .database import db

class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    email_id = db.Column(db.String, unique=True, nullable=False)
    
    # webhook_url = db.Column(db.String, unique=True, nullable=True)
    # app_preferences = db.Column(db.String, nullable=False)

    def __init__(self, user_id, username, password, email_id):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email_id = email_id

    def to_dict(self):
        return dict(id=self.user_id, username=self.username, password=self.password, email_id=self.email_id, phone_no=self.phone_no, webhook_url=self.webhook_url, app_preferences=self.app_preferences, user_preferences=self.user_preferences)

