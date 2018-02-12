from flask_restful import Resource
from project.extra import login_required,checke_interface
from project.models import User,Praise
from flask import request,g,jsonify

class post_card(Resource):
    #发布动态接口----------------------------
    #给卡片，时间戳13位、内容、图片（数组）、状态、tags、share（Bool）
    @login_required
    def post(self):
        card_dict = g.user.verify_data(request.json,"create_card")
        #这块还要修改
        g.user.create_card(card_dict)
        g.user.insert()

        #用于调试查看的
        print ("content:%s,images:" % \
            (card_dict['content']),\
            card_dict['images'])

        return jsonify(status = 1,\
                    message = "success")

class praise_interface(Resource):
    #点赞接口------------------------------
    @login_required
    def post(self):
        praise = Praise()
        if request.json['action'] is 1:
            praise.create_praise(request.json['card_id'],\
                                g.user.get_user_id())
            return jsonify(status = 1,\
                        message = "success")
        elif request.json['action'] is 0:
            praise.del_praise(request.json['card_id'],\
                                g.user.get_user_id())
            return jsonify(status = 1,\
                        message = "success")
        else:
            return jsonify(status = 0,\
                        message = "failed")

class card_comment(Resource):
    #评论接口------------------------------
    #还未完成
    #内容、卡片ID、回复（被回复者昵称）、是否直接评论作者（Bool）、时间戳
    @login_required
    def post(self):
        comments_dict = request.json
        comments_dict['user_id'] = g.user.get_user_id()
        
        return jsonify(status = 1,\
                    message = "success")

class user_get_card(Resource):
    #用户自己的动态获取接口
    @login_required
    def post(self):
        return jsonify(status = 1,\
                    message = "success")
    #卡片组：发布人头像，昵称，ID，时间，关注与否、点赞与否、内容、状态、tag、赞数、评论数、图片、卡片id、用户id
    #关于卡片，细节多给：评论者ID、评论者头像、昵称、内容、日期

class guest_get_card(Resource):
    #访客随机获取的动态接口

    def post(self):
        return jsonify(status = 1,\
                    message = "success")
