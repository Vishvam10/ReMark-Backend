from application.database import db

from sqlalchemy.sql import func

class Annotation(db.Model):
    __tablename__ = "annotation"

    annotation_id = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    annotation_name = db.Column(db.String, nullable=False)

    # STORE THIS AS ENV VARIABLE (FOR ADMINS)
    website_id = db.Column(db.String, nullable=False)

    # https://somesite.com/articles/34md23j4#selected1
    # ------------ URL -------------
    # ---------------------- URI ---------------------
    
    # URI changes a lot especially for SPAs
    
    website_uri = db.Column(db.String, unique=False, nullable=False)
    html_node_data_tag = db.Column(db.String, unique=True, nullable=False)

    tags = db.Column(db.String, unique=False, nullable=True)
    resolved = db.Column(db.Boolean, unique=False, default=False)
    
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now()) 

    created_by = db.Column(db.String, unique=False, nullable=False)

    comments = db.relationship('Comment', backref='annotation', lazy=True)

    def to_dict(self):
        return dict(annotation_id=self.annotation_id, website_id=self.website_id, website_uri=self.website_uri, html_node_data_tag=self.html_node_data_tag, created_at=self.created_at, updated_at=self.updated_at, created_by=self.created_by)

