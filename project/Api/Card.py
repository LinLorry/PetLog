from urllib import parse
from flask_restful import Resource
from flask import request, g, jsonify
from project.Models.User import User
from project.Models.Card import Card
from project.Models.Tag import Tag
from project.extra import login_required, checke_interface, verify_auth_token


# 获取tags的接口
class get_tags(Resource):
    @checke_interface
    def get(self):
        tag = Tag()
        all_tag = tag.all_tags()
        re = {"status": 1, "tags": all_tag}
        return jsonify(re)


# 发布卡片的接口
class post_card(Resource):
    #发布动态接口----------------------------
    #给卡片，时间戳13位、内容、图片（数组）、状态、tags、share（Bool）
    @login_required
    def post(self):
        if g.user.create_card(request.json):
            return jsonify(status=1, message="success")
        else:
            return jsonify(status=0, message="failed")


# 点赞的接口
class praise_interface(Resource):
    #点赞接口------------------------------
    @login_required
    def post(self):
        if (request.json['action'] == 1 or \
            request.json['action'] == 0 )and \
            g.user.user_praise(request.json['id'],
                               request.json['action']):
            return jsonify(status=1, message="点赞成功！")
        else:
            return jsonify(status=0, message="点赞失败，请重试！")


# 评论的接口
class card_comment(Resource):
    # ------------------------------>评论接口
    @login_required
    def post(self):
        time = g.user.create_comment(request.json)
        if time:
            return jsonify(status=1, message="发表评论成功！", time=time)
        else:
            return jsonify(status=0, message="发表评论失败，请重试！")


# 用户获取朋友圈接口
class u_get_circle_of_friends(Resource):
    @login_required
    def get(self):
        re = request.query_string.decode('utf-8')
        re = parse.parse_qs(re)
        try:
            re['tag']
        except KeyError:
            re['tag'] = None
        if re['lastCursor'][0] == "none":
            re['lastCursor'][0] = None

        c_o_f = g.user.get_circle_of_friends(re['tag'], re['lastCursor'][0])
        c_o_f['status'] = 1
        return jsonify(c_o_f)


# 用户获取时间轴的接口
class u_get_timeline(Resource):
    @login_required
    def get(self):
        re = request.query_string.decode('utf-8')
        re = parse.parse_qs(re)
        timeline = g.user.get_timeline(re['id'][0])
        if timeline:
            timeline['status'] = 1
            timeline['message'] = "获取成功"
            return jsonify(timeline)
        else:
            return jsonify(status=0, message="你没有权限获取该宠物的时间轴")


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
            return jsonify(status=0, message="你没有权限获取该动态的详细内容")


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
        token = request.headers.get("Authorization")
        if token:
            if verify_auth_token(token):
                hot = g.user.get_hot_card(re['tag'])
            else:
                return jsonify(status=0, message="请重新登录")
        else:
            user = User()
            hot = user.get_hot_card(re['tag'])
        hot['status'] = 1
        return jsonify(hot)


class get_other_all_cards(Resource):
    @login_required
    def get(self):
        re = request.query_string.decode('utf-8')
        re = parse.parse_qs(re)

        if re['lastCursor'][0] == "none":
            re['lastCursor'][0] = None

        cards = g.user.get_user_all_card(re['id'][0], re['lastCursor'][0])
        if cards:
            res = {"status": 1, "infinited": False, "cards": cards}
            if len(cards) < 5:
                res['infinited'] = True
            return jsonify(res)
        else:
            return jsonify(status=0, message="failed")
