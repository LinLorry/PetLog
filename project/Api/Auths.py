from flask import request,make_response,g,current_app,jsonify
from flask_restful import Resource
from project.models import User
from project.extra import login_required

class auth(Resource):
    def post(self):
        try:
            user = User()
            user_data = user.verify_data(request.json,"auth")
            user.select(user_data)
            if user.verify_password(user_data['password']):
                return jsonify(status = 1, \
                        token = user.generate_auth_token().decode("utf8"))
            else:
                return jsonify(status = 0, \
                        message = "failed")
        except:
            return jsonify(status =0, \
                    message = "failed")

class use_auth(Resource):
    @login_required
    def post(self):
        return jsonify(status = 1, message = "success")

