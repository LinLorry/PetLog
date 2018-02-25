from urllib import parse
from flask_restful import Resource
from flask import request,g,jsonify
from project.Models.User import User
from project.Models.Card import Card
from project.Models.Tag import Tag
from project.extra import login_required,checke_interface

#获取tags的接口
class get_tags(Resource):
    @checke_interface
    def get(self):
        tag = Tag()
        all_tag = tag.all_tags()
        re = {
            "status":1,
            "tags":all_tag
        }
        return jsonify(re)

#发布卡片的接口
class post_card(Resource):
    #发布动态接口----------------------------
    #给卡片，时间戳13位、内容、图片（数组）、状态、tags、share（Bool）
    #这块还要修改
    @login_required
    def post(self):
        if g.user.create_card(request.json):
            return jsonify(status = 1,
                        message = "success")
        else:
            return jsonify(status = 0,
                        message = "failed")

#点赞的接口
class praise_interface(Resource):
    #点赞接口------------------------------
    @login_required
    def post(self):
        if (request.json['action'] == '1' or \
            request.json['action'] == '0' )and \
            g.user.user_praise(request.json['id'],
                               request.json['action']):
            return jsonify(status = 1,
                        message = "success")
        else:
            return jsonify(status = 0,
                        message = "failed")

#评论的接口
class card_comment(Resource):
    # ------------------------------>评论接口
    #还未完成
    #回复（被回复者昵称）、是否直接评论作者（Bool）、时间戳
    @login_required
    def post(self):
        time = g.user.create_comment(request.json)
        if time:
            return jsonify(status = 1,
                        message = "success",
                        time = time)
        else:
            return jsonify(status = 0,
                        message = "failed")

# 用户获取朋友圈接口
class u_get_circle_of_friends(Resource):
    @login_required
    def post(self):

        re = request.query_string.decode('utf-8')
        re = parse.parse_qs(re)
        try:
            re['tag']
        except KeyError:
            re['tag'] = None
        try:
            re['lastCursor']
        except KeyError:
            re['lastCursor']=None
            
        c_o_f = g.user.get_circle_of_friends(re['tag'],re['lastCursor'])
        c_o_f['status'] = 1
        return jsonify(c_o_f)

# 用户获取时间轴的接口
class u_get_timeline(Resource):
    @login_required
    def post(self):
        timeline = g.user.get_timeline(request.json['pet_id'])
        timeline['status'] = 1
        timeline['message'] = "获取成功"
        if timeline:
            return jsonify(timeline)
        else:
            return jsonify(status = 0,message = "你没有权限获取该宠物的时间轴")

# 用户获取卡片的详细内容
class u_get_card_detail(Resource):
    @login_required
    def get(self):
        re = request.query_string.decode('utf-8')
        re = parse.parse_qs(re)
        card_detail = g.user.get_card_detail(re['id'])
        if card_detail:
            return jsonify(card_detail)
        else:
            return jsonify(status = 0,message = "你没有权限获取该动态的详细内容")

# 热门动态接口
class get_hot_card(Resource):
    @checke_interface
    def get(self):
        re = request.query_string.decode('utf-8')
        re = parse.parse_qs(re)
        try:
            re['tag']
        except KeyError:
            re['tag'] = None
        user = User()
        hot = user.get_hot_card(re['tag'])
        hot['status'] = 1
        return jsonify(hot)

# ----------------------------->访客的接口

class g_get_timeline(Resource):
    @checke_interface
    def post(self):
        user = User(option="guest")
        user.verify_data(request.json,"get_timeline")
        return jsonify(g.user.get_timeline(request.json['pet_id']))

# 访客获取卡片的详细内容
class g_get_card_detail(Resource):
    @login_required
    def get(self,card_id):
        card = Card()
        return jsonify(card.get_detail(card_id))

# 访客随机获取的动态接口
class g_get_card(Resource):
    def post(self):
        card = Card()
        return jsonify(card.get_hot_card())


#---------------->有问题的接口
''' # 用户获取他人宠物时间轴的接口
class user_get_other_pet_timeline(Resource):
    @login_required
    def post(self):
        g.user.verify_data(request.json,"get_timeline")
        return jsonify(g.user.get_timeline(request['pet_id'])) '''

''' # 获取宠物的卡片，方法会对用户是否可以获取卡片判断
class get_pet_card(Resource):
    @login_required
    def post(self):
        return jsonify(g.user.get_pet_card(request.json['pet_id'])) '''



