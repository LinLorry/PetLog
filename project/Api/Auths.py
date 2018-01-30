from flask import request,make_response,g,current_app,jsonify
from flask_restful import Resource
from project.models import User

class auth(Resource):
    def post(self):
        #创建用户对象
        user = User(request.json.get('username'))
        
        if user.verify_password(request.json.get('password')):
            g.user = user
            rst = make_response() 
            rst.headers['Authorization'] = g.user.generate_auth_token()
            return rst
        else:
            return jsonify(status = 0,message = "failed")
