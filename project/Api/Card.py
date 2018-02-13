from flask_restful import Resource
from project.extra import login_required,checke_interface
from project.models import User,Praise
from flask import request,g,jsonify

class post_card(Resource):
    #发布动态接口----------------------------
    #给卡片，时间戳13位、内容、图片（数组）、状态、tags、share（Bool）
    @login_required
    def post(self):
        #这块还要修改
        if g.user.create_card(request.json):
            # 用于调试查看的
            print ("content:%s,images:" % (
                    request.json['content']) +
                    request.json['images'])

            return jsonify(status = 1,
                        message = "success")
        else:
            return jsonify(status = 0,
                        message = "failed")

class praise_interface(Resource):
    #点赞接口------------------------------
    @login_required
    def post(self):
        if (request.json['action'] == '1' or \
            request.json['action'] == '0' )and \
            g.user.user_praise(request.json['card_id'],
                               request.json['action']):
            return jsonify(status = 1,
                        message = "success")
        else:
            return jsonify(status = 0,
                        message = "failed")

class card_comment(Resource):
    #评论接口------------------------------
    #还未完成
    #回复（被回复者昵称）、是否直接评论作者（Bool）、时间戳
    @login_required
    def post(self):
        g.user.create_comment(request.json)
        # 用于调试查看的
        print("content:%s,images:%s" % (
                request.json['content'],
                request.json['bool']))
        return jsonify(status = 1,
                    message = "success")

class user_get_card(Resource):
    #用户自己的动态获取接口
    @login_required
    def post(self):
        friend_card = g.user.get_friend_card(request.json)
        return jsonify(card=friend_card)
    #卡片组：发布人头像，昵称，ID，时间，关注与否、点赞与否、内容、状态、tag、赞数、评论数、图片、卡片id、用户id
    #关于卡片，细节多给：评论者ID、评论者头像、昵称、内容、日期

class guest_get_card(Resource):
    #访客随机获取的动态接口

    def post(self):
        return jsonify(status = 1,
                    message = "success")
