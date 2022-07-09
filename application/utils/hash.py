import bcrypt

def createHashedPassword(password) :
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

def checkHashedPassword(password, hashed_password) :
    return bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8')