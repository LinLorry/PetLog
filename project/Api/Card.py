from flask_restful import Resource
from project.extra import login_required
from project.models import User
from flask import request,g,jsonify

class post_card(Resource):
    #发布动态接口
    @login_required
    def post(self):
        try:
            card_dict = g.user.verify_data(request.json,"create_card")
            g.user.create_card(card_dict)
            g.user.insert()

            '''if not (card_dict['content'].strip() or \
                    card_dict['images'].strip()):
                return jsonify(status = 0,\
                message = "content and image can't exist at the same time.")
            '''
            #用于调试查看的
            print ("content:%s,images:" % \
                (card_dict['content']),\
                card_dict['images'])
        except:
            return jsonify(status =0, \
                    message = "failed")
        else:
            return jsonify(status = 1,message = "success")

class card_comment(Resource):
    @login_required
    def post(self):
        try:
            comments_dict = request.json
            
        except:
            return jsonify(status = 0, \
                    message = "failes")

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
