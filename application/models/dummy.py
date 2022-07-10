from application.database import db

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String)
