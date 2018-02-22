import re
import os
import md5, uuid
from flask import jsonify, g, request, current_app, Response
from werkzeug import secure_filename
from flask_restful import Resource
from project.Models.Follow import Follow
from project.Models.User import User
from project.extra import login_required, checke_interface, allowed_file

re_follow = re.compile(r'^action\=(\d)\&lastCursor\=\$(.*)$')

class follow_interface(Resource):
    @login_required
    def get(self):
        r = re_follow.match(request.query_string.decode('utf-8'))

        be_concerned_id = r.group(2)
        follow_operation = r.group(1)

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

class user_information(Resource):
    @login_required
    def get(self):
        return jsonify(g.user.get_information())

class user_other_information(Resource):
    @login_required
    def post(self):
        return jsonify(g.user.get_other_information
                (request.json['user_id']))

class guest_get_information(Resource):
    @checke_interface
    def post(self):
        user = User("guest")
        return jsonify(user.get_other_information
                (request.json['user_id']))

class upload_avatar(Resource):
    #上传卡片图像的类
    @login_required
    def post(self):
        file = request.files['image']
        if file and allowed_file(file.filename):
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