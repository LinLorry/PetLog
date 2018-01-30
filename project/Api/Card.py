from flask_restful import Resource
from project.extra import login_required
from project.models import User
from flask import request,g,jsonify

class post_card(Resource):
    #发布动态接口

    @login_required
    def post(self):
        card_dict = request.json

        #内容和图片不能同时没有
        if not card_dict['content'] and \
            not card_dict['images']:
            return jsonify(status = 0,\
                message = "content and image can't exist at the same time.")
        #动态发布一定要有时间
        elif not card_dict['time']:
            return jsonify(status = 0,\
                message = "card must has time")
        else:
            g.user.create_card(request.json)
            return jsonify(status = 1,\
                message = "success")

class user_get_card(Resource):
    #用户自己的动态获取接口

    @login_required
    def post(self):
        return jsonify(status = 1,\
                message = "success")

class guest_get_card(Resource):
    #访客随机获取的动态接口

    def post(self):
        return jsonify(status = 1,\
                message = "success")
