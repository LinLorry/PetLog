from flask_restful import Resource
from flask import jsonify, g, request
from project.extra import login_required

class create_pet(Resource):
    @login_required
    def post(self):
        if g.user.create_pet(request.json):
            return jsonify(status = 1, message = "success")
        else :
            return jsonify(status = 0, message = "failed")

class get_user_all_pet(Resource):
    @login_required
    def get(self):
        request.query_string.decode('utf-8')
        pet_list = {
            "status":1,
            "pets":g.user.get_user_pets()
        }
        if pet_list:
            return jsonify(pet_list = pet_list)
        else:
            return jsonify(status = 0, message = "failed")