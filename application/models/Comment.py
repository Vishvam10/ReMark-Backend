import datetime

from dataclasses import dataclass
from application.database.dev.database import db

from sqlalchemy.sql import func


@dataclass
class Comment(db.Model): 
    
    comment_id : str
    annotation_id : str
    content : str
    content_html : str

    parent_node : str

    upvotes : int
    downvotes : int
    
    mod_required : bool
    
    created_at : datetime.datetime
    updated_at : datetime.datetime

    created_by_id : str
    created_by : str
    
    __tablename__ = "comment"

    comment_id = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    annotation_id = db.Column(db.String, db.ForeignKey('annotation.annotation_id'), nullable=False)
    content = db.Column(db.String, unique=False, nullable=False)
    content_html = db.Column(db.String, unique=False, nullable=True)

    parent_node = db.Column(db.String, unique=False, nullable=True)

    upvotes = db.Column(db.Integer, unique=False, nullable=True)
    downvotes = db.Column(db.Integer, unique=False, nullable=True)
    
    mod_required = db.Column(db.Boolean, unique=False, default=False)
    
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now(), server_default=func.now()) 

    created_by_id = db.Column(db.String, db.ForeignKey('user.user_id'))
    created_by = db.Column(db.String, unique=False, nullable=False)

    def to_dict(self):
        return dict(comment_id=self.comment_id, content=self.content, content_html=self.content_html, parent_node=self.parent_node, upvotes=self.upvotes, downvotes=self.downvotes, mod_required=self.mod_required, created_at=self.created_at, updated_at=self.updated_at, created_by=self.created_by, created_by_id=self.created_by_id)

