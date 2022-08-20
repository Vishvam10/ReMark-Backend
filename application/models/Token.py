from dataclasses import dataclass
from application.database.database import db

@dataclass
class Token(db.Model):
    user_id : str
    api_key : str

    __tablename__ = "token"

    user_id = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    api_key = db.Column(db.String, unique=True, nullable=False)

    def to_dict(self):
        return dict(user_id=self.user_id, api_key=self.api_key)

