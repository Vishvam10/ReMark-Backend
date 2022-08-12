import datetime

from dataclasses import dataclass

from application.database.database import db

from sqlalchemy.sql import func

@dataclass
class Annotation(db.Model):
    __tablename__ = "annotation"

    annotation_id : str
    annotation_name : str
    website_id : str    
    website_uri : str 
    node_xpath : str 
    html_id : str 
    html_tag : str 
    html_text_content : str 
    tags : str 
    resolved : bool

    created_at : datetime.datetime
    updated_at : datetime.datetime

    created_by_id : str
    created_by : str
    
    modified_by_id : str
    modified_by : str
    
    comments : list

    annotation_id = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    annotation_name = db.Column(db.String, nullable=False)

    # STORE THIS AS ENV VARIABLE (FOR ADMINS)
    website_id = db.Column(db.String, nullable=False)

    # https://somesite.com/articles/34md23j4#selected1
    # ------------ URL -------------
    # ---------------------- URI ---------------------
    
    # URI changes a lot especially for SPAs
    
    website_uri = db.Column(db.String, unique=False, nullable=False)
    node_xpath = db.Column(db.String, unique=False, nullable=False)
    html_id = db.Column(db.String, unique=True, nullable=True)
    html_tag = db.Column(db.String, unique=False, nullable=True)
    html_text_content = db.Column(db.String, unique=False, nullable=True)

    tags = db.Column(db.String, unique=False, nullable=True)
    resolved = db.Column(db.Boolean, unique=False, default=False)
    
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now(), server_default=func.now()) 

    created_by_id = db.Column(db.String, db.ForeignKey('user.user_id'))
    created_by = db.Column(db.String, unique=False, nullable=False)

    modified_by_id = db.Column(db.String, db.ForeignKey('user.user_id'), nullable=True)
    modified_by = db.Column(db.String, unique=False, nullable=True)

    comments = db.relationship('Comment', backref='annotation', lazy=True)

    def to_dict(self):
        return dict(annotation_id=self.annotation_id, website_id=self.website_id, website_uri=self.website_uri, node_xpath=self.node_xpath, html_id=self.html_id, html_tag=self.html_tag, html_text_content=self.html_text_content, created_at=self.created_at, updated_at=self.updated_at, created_by_id=self.created_by_id, created_by=self.created_by, modified_by_id=self.modified_by_id, modified_by=self.modified_by)

