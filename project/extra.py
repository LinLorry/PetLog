from flask import request,abort,current_app,g,jsonify
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired,BadSignature
from .models import User

def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):

        def verify_auth_token(token):
            s = Serializer(current_app.config['SECRET_KEY'])
            try:
                data = s.loads(token)
            except SignatureExpired:
                return None # valid token, but expired
            except BadSignature:
                return None # invalid token
            g.user = User(data['username'])
            return True

        token = request.headers.get("Authorization")

        if not token:
            return jsonify(status = 0,message = "failed")
        else :
            if verify_auth_token(token):
                return func(*args, **kwargs)
            else:
                return jsonify(status = 0,message = "failed")
    return inner