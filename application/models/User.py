import datetime

from dataclasses import dataclass
from email.policy import default
from application.database.database import db

from sqlalchemy.sql import func

@dataclass
class User(db.Model):
    __tablename__ = "user"

    user_id : str
    username : str
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

    # Comma separated strings : comment_id1, comment_id2, . . .
    
    upvotes = db.Column(db.String, unique=False, nullable=True, default="none")    
    downvotes = db.Column(db.String, unique=False, nullable=True, default="none")    

    def to_dict(self):
        return dict(user_id=self.user_id, username=self.username, email_id=self.email_id, created_at=self.created_at, modified_at=self.modified_at, authority=self.authority, upvotes=self.upvotes, downvotes=self.downvotes)