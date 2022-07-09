from enum import Flag
from application.database import db

from sqlalchemy.sql import func

class Annotations(db.Model):
    __tablename__ = "annotations"

    annotation_id = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    content = db.Column(db.String, unique=False, nullable=False)
    html_content = db.Column(db.String, unique=False, nullable=False)
    parent_node = db.Column(db.String, unique=False, nullable=True)

    tags = db.Column(db.String, unique=False, nullable=True)
    upvotes = db.Column(db.Integer, unique=False, nullable=True)
    downvotes = db.Column(db.Integer, unique=False, nullable=True)
    
    mod_required = db.Column(db.Boolean, unique=False, default=False)
    
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now()) 

    def to_dict(self):
        return dict(id=self.annotation_id, content=self.content, html_content=self.html_content, parent_node=self.parent_node, tags=self.tags, upvotes=self.upvotes, downvotes=self.downvotes, mod_required=self.mod_required, created_at=self.created_at, updated_at=self.updated_at)

