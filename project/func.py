#关于token的文件，还未完成

from flask_jwt import JWT, jwt_required, current_identity
from .models import User
from manage import app

def authenticate(username):
    return username

def identity(userid):
    return userid
