import datetime

from dataclasses import dataclass
from application.database import db

from sqlalchemy.sql import func

@dataclass
class User(db.Model):
    __tablename__ = "user"

    user_id : str
    username : str
    password : str
    email_id : str
    bio : str
    authority : str
    created_at : datetime.datetime
    modified_at : datetime.datetime

    user_id = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    email_id = db.Column(db.String, unique=True, nullable=False)

    bio = db.Column(db.String, unique=False, nullable=True)
    
    authority = db.Column(db.String, unique=False, nullable=False)    
    
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    modified_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

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

    # def to_dict(self):
    #     return dict(id=self.user_id, username=self.username, password=self.password, email_id=self.email_id, created_at=self.created_at, modified_at=self.modified_at, authority=self.authority, api_key=self.api_key)
