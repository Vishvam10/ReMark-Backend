from application.database import db

from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    email_id = db.Column(db.String, unique=True, nullable=False)
    
    authority = db.Column(db.String, unique=True, nullable=False)
    api_key = db.Column(db.String, unique=True, nullable=False)
    
    
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now()) 

    webhook_url = db.Column(db.String, unique=True, nullable=True)
    app_preferences = db.Column(db.String, nullable=False)

    # def __init__(self, user_id, username, password, email_id, authority, api_key, created_at, updated_at, webhook_url, app_preferences):
    #     self.user_id = user_id
    #     self.username = username
    #     self.password = password
    #     self.email_id = email_id

    #     self.authority = authority
    #     self.api_key = api_key

    #     self.created_at = created_at
    #     self.updated_at = updated_at

    #     self.webhook_url = webhook_url
    #     self.app_preferences = app_preferences

    def to_dict(self):
        return dict(id=self.user_id, username=self.username, password=self.password, email_id=self.email_id, webhook_url=self.webhook_url, app_preferences=self.app_preferences, user_preferences=self.user_preferences)

