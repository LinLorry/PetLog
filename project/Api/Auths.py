from flask import request,make_response,g
from flask_restful import Resource
from project.models import User

class auth(Resource):
    def post(self):
        #创建用户对象
        user = User(request.json.get('username'))
        ''' if user.verify_password(request.json.password):
            g.user = user'''
        rst = make_response() 
        rst.headers['Authorization'] = "222344cgvhjuytub789vry"
        #g.user.generate_auth_token()
        return rst
        ''' else:
            return "failure" '''
