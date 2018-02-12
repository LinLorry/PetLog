import random
from flask import request,abort,current_app,g,jsonify,render_template
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired,BadSignature
from .models import User
from flask_mail import Message
from . import mail



def checke_interface(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return jsonify(status = 0,\
                        message = "failed")
    return inner

@checke_interface
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
            g.user = User()
            g.user.select(data)
            #g.user.find_user(data['email'])
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

def send_email(to_mail):
    msg  = Message("Hello",recipients = [to_mail])
    code = ''.join(random.sample([chr(i) for i in range(65,91)],5))
    msg.html = render_template("./static/mail.html",code = code)
    mail.send(msg)