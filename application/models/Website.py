from dataclasses import dataclass
from application.database import db

@dataclass
class Website(db.Model):
    website_id : str
    website_url : str
    admin : str
    admin_type : str
    n_annotations : int
    annotation_limit : int

    __tablename__ = "website"

    website_id = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    website_url = db.Column(db.String, unique=False, nullable=False)

    n_annotations = db.Column(db.Integer, unique=False, nullable=True)
    annotation_limit = db.Column(db.Integer, unique=False, nullable=True) 

    admin = db.Column(db.String, unique=True, nullable=False)
    admin_type = db.Column(db.String, unique=False, nullable=False)


    def to_dict(self):
        return dict(website_id=self.website_id, website_url=self.website_url, n_annotations=self.n_annotations, annotation_limit=self.annotation_limit, admin=self.admin, admin_type=self.admin_type)

