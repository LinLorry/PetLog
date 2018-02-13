from flask import request,make_response,g,current_app,jsonify
from flask_restful import Resource
from project.models import User
from project.extra import login_required,checke_interface

class auth(Resource):
    @checke_interface
    def post(self):

        user = User()
        user_data = user.verify_data(request.json,"auth")
        #user.find_user(user_data['email'])
        user.select(user_data)
        if user.verify_password(user_data['password']):
            return jsonify(status = 1, \
                        token = user.generate_auth_token().decode("utf8"))
        else:
            return jsonify(status = 0, \
                        message = "failed")


class use_auth(Resource):
    @login_required
    def post(self):
        return jsonify(status = 1, \
                    message = "success")

