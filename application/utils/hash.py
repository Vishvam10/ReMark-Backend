import string
import random
import bcrypt

def create_hashed_password(password) :
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

def check_hashed_password(password, hashed_password) :
    return bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8'))

def generate_api_key(length):
    char_set = string.ascii_letters + string.punctuation                    
    urand = random.SystemRandom()                                           
    return ''.join([urand.choice(char_set) for _ in range(length)])