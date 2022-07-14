from application.database import db

from sqlalchemy.sql import func

class Annotation(db.Model):
    __tablename__ = "annotation"

    annotation_id = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    website_id = db.Column(db.String, unique=True, nullable=False, primary_key=True)

    
    # https://somesite.com/articles/34md23j4#selected1
    # ------------ URL -------------
    # ---------------------- URI ---------------------
    
    # URI changes a lot especially for SPAs

    website_url = db.Column(db.String, unique=False, nullable=False)
    website_uri = db.Column(db.String, unique=False, nullable=False)

    html_node_id = db.Column(db.String, unique=True, nullable=False)

    content = db.Column(db.String, unique=False, nullable=False)
    content_html = db.Column(db.String, unique=False, nullable=False)

    parent_node = db.Column(db.String, unique=False, nullable=True)

    tags = db.Column(db.String, unique=False, nullable=True)
    upvotes = db.Column(db.Integer, unique=False, nullable=True)
    downvotes = db.Column(db.Integer, unique=False, nullable=True)
    
    
    resolved = db.Column(db.Boolean, unique=False, default=False)

    mod_required = db.Column(db.Boolean, unique=False, default=False)
    
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now()) 

    created_by = db.Column(db.String, unique=False, nullable=False)

    def to_dict(self):
        return dict(annotation_id=self.annotation_id, content=self.content, html_content=self.html_content, parent_node=self.parent_node, tags=self.tags, upvotes=self.upvotes, downvotes=self.downvotes, mod_required=self.mod_required, created_at=self.created_at, updated_at=self.updated_at)

