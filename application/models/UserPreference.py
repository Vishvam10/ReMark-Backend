from dataclasses import dataclass
from application.database.database import db

# ONLY FOR ADMINS

@dataclass
class UserPrefence(db.Model):
    __tablename__ = "user_preference"

    user_id : str
    show_resolved : bool
    show_moderated_comments : bool
    comments_limit_per_annotation : int
    default_theme : str
    brand_colors : str
  
    user_id = db.Column(db.String, unique=True, nullable=False, primary_key=True)

    show_resolved = db.Column(db.Boolean, unique=False, default=False)
    show_moderated_comments = db.Column(db.Boolean, unique=False, default=False)
    comments_limit_per_annotation = db.Column(db.Integer, unique=False, default=10)    

    default_theme = db.Column(db.String, unique=False, default="light")

    # This is a JSON string 
    brand_colors = db.Column(db.String, unique=False, nullable=True)

   
    def to_dict(self):
        return dict(user_id=self.user_id, show_resolved=self.show_resolved, show_moderated_comments=self.show_moderated_comments, comments_limit_per_annotation=self.comments_limit_per_annotation, default_theme=self.default_theme, brand_colors=self.brand_colors)