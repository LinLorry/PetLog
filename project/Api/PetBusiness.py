import uuid
import os
from hashlib import md5
from urllib import parse
from werkzeug import secure_filename
from flask_restful import Resource
from flask import jsonify, g, request, current_app
from project.extra import login_required, allowed_image, checke_interface


class create_pet(Resource):
    @login_required
    def post(self):
        pet_id = g.user.create_pet(request.json)
        if pet_id:
            return jsonify(status=1, message="宠物信息创建成功！", id=pet_id)
        else:
            return jsonify(status=0, message="创建宠物信息失败，请重试！")


class update_pet(Resource):
    @login_required
    def post(self):
        if g.user.update_pet(request.json):
            return jsonify(status=1, message="更新宠物信息成功！")
        else:
            return jsonify(status=0, message="更新宠物信息失败，请重试！")


class get_user_all_pet(Resource):
    @login_required
    def get(self):
        pet_list = g.user.get_all_pets()
        if pet_list:
            return jsonify(pet_list)
        else:
            return jsonify(status=0, message="获取宠物列表失败，请重试！")


class pet_avatar(Resource):
    @login_required
    def post(self):
        file = request.files['image']
        if file and allowed_image(file.filename):
            #str1是随机的uuid
            #str2是图片名
            #str3是图片的后缀
            str1 = str(uuid.uuid1()).split("-")[0]
            str2 = secure_filename(file.filename).rsplit('.')[0]
            str3 = '.' + file.filename.rsplit('.')[1]

            m = md5()
            m.update((str1 + str2).encode('utf-8'))

            filename = str(m.hexdigest()) + str3

            file.save(
                os.path.join(current_app.config['PET_AVATAR_FOLDER'],
                             filename))

            #文件上传成功，返回文件名
            return jsonify(status = 1,\
                    filename = filename)
        else:
            return jsonify(status = 0,\
                        message = "failed")


class get_pet_detail(Resource):
    @login_required
    def get(self):
        re = request.query_string.decode('utf-8')
        id = parse.parse_qs(re)['id']
        pet_detail = g.user.get_pet_detail(id)
        return jsonify(pet_detail)
