from application.database import db
from application.models.User import User


# def get_random_admin() :
#     users = db.session.query(User).all()
#     for user in users :
#         authority = user.__dic__["authority"]
#         if(authority == "admin") :
#             print(user)