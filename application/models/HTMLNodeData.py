from application.database import db

from sqlalchemy.sql import func

class HTMLNodeData(db.Model):
    __tablename__ = "html_node_data"

    website_id = db.Column(db.String, unique=True, nullable=False, primary_key=True)

    website_url = db.Column(db.String, unique=False, nullable=False)
    html_node = db.Column(db.String, unique=False, nullable=False)
    html_parent_node = db.Column(db.String, unique=False, nullable=True)
    html_node_class = db.Column(db.String, unique=False, nullable=True)
    html_node_id = db.Column(db.String, unique=False, nullable=True)

    # depth_from_body = db.Column(db.Integer, unique=False, nullable=True)

    annotation_id = db.Column(db.String, db.ForeignKey("annotation.annotation_id"), nullable=False)

    def to_dict(self):
        return dict(annotation_id=self.annotation_id, website_id=self.website_id, website_url=self.website_url, html_node=self.html_node, html_parent_node=self.html_parent_node, html_node_class=self.html_node_class, html_node_id=self.html_node_id)

