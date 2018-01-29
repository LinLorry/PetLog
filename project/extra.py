from flask import request,abort
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):

        def verify_auth_token(token):
            s = Serializer("ssss")
                ''' app.config['SECRET_KEY']) '''
            try:
                data = s.loads(token)
            except SignatureExpired:
                return None # valid token, but expired
            except BadSignature:
                return None # invalid token
            return True

        token = request.headers.get("Authorization")

        if not token:
            abort(403, "login in first")
        else :
            if verify_auth_token(token):
                return func(*args, **kwargs)
            else:
                return abort(403,"please login")
    return inner