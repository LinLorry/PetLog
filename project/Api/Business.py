
import os
import uuid
from hashlib import md5
from urllib import parse
from flask import jsonify, g, request, current_app, Response
from werkzeug import secure_filename
from flask_restful import Resource
from project.Models.Follow import Follow
from project.Models.User import User
from project.extra import login_required, checke_interface, allowed_image

class follow_interface(Resource):
    @login_required
    def get(self):
        be_concerned_id = request.json['following_id']
        follow_operation = request.json['action']

        if follow_operation == '1' and \
            g.user.user_follow(be_concerned_id,follow_operation):
            return jsonify(status=1,
                            action_status=1,
                            message="关注成功")
        elif follow_operation == '0' and \
            g.user.user_follow(be_concerned_id, follow_operation):
                return jsonify(status=1,
                               action_status=1,
                               message="取消关注成功")
        else:
            return jsonify(status=0, message="failed")

class get_followers(Resource):
    @login_required
    def get(self):
        followers = g.user.get_followers()
        return jsonify(
            status = 1,
            message = "获取成功",
            followers = followers
            )
            
class get_followings(Resource):
    @login_required
    def get(self):
        followings = g.user.get_followings()
        return jsonify(
            status = 1,
            message = "获取成功",
            followings = followings
        )

class user_profile_summary(Resource):
    @login_required
    def get(self):
        profile_summary = g.user.get_profile_summary()
        res = {
            "status": 1,
            "message":"获取成功",
            "user":profile_summary
        }
        return jsonify(res)

class user_profile(Resource):
    @login_required
    def get(self):
        profile = g.user.get_profile()
        res = {
            "status": 1,
            "message": "获取成功",
            "user1": profile
        }
        return jsonify(res)

class user_other_profile(Resource):
    @login_required
    def post(self):
        re = request.query_string.decode('utf-8')
        re = parse.parse_qs(re)

        other_profile = g.user.get_other_profile(re['id'])
        if other_profile:
            other_profile['status'] = 1
            other_profile['message'] = "获取成功"
            return jsonify(other_profile)
        else:
            return jsonify(status = 0,\
                        message = "failed")

class update_user(Resource):
    @login_required
    def post(self):
        mesage = g.user.update_user(request.json)
        if mesage:
            return jsonify(status = 1,message = "success")
        else:
            return jsonify(status = 0,message = mesage)

class upload_avatar(Resource):
    #上传卡片图像的类
    @login_required
    def post(self):
        file = request.files['image']
        if file and allowed_image(file.filename):
            #str1是用户的id
            #str2是图片的后缀
            str1 = str(uuid.uuid1()).split("-")[0]
            str2 = secure_filename(file.filename).rsplit('.')[0]
            str3 = '.' + file.filename.rsplit('.')[1]

            m = md5()
            m.update((str1 + str2).encode ('utf-8'))

            filename = m.hexdigest()[-8:8] + str3

            filename = str1 + str2

            file.save (os.path.join(
                current_app.config['USERHEAD_IMAGES_FOLDER'],
                filename))
        else:
            return jsonify(status = 0,\
                        message = "failed")

        #文件上传成功，返回文件名
        return jsonify(status = 1,\
                    filename = filename)

class guest_get_information(Resource):
    @checke_interface
    def post(self):
        user = User("guest")
        return jsonify(user.get_other_information
                (request.json['user_id']))