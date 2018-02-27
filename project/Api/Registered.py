import os
import uuid
import random
from hashlib import md5
from werkzeug import secure_filename
from flask_restful import Resource
from flask import jsonify, request, current_app
from project.Models.User import User
from project.Models.PetLogDataError import PetLog_DataError
from project.extra import send_registered_email, checke_interface, allowed_image


class registered(Resource):
    @checke_interface
    def post(self):
        if self.verify_code(request.json):
            user = User()
            user_dict = User.verify_data(request.json,verify_type = 'register')
            user.create_user(user_dict)
            user.insert()

            return jsonify(status=1,
                        message="success")
        else:
            return jsonify(status=0,
                        message='failed')

    def verify_code(self, code_dict):
        #str1 是用户的email
        #str2 是注册使用的密钥
        #str3 是用户的密码
        str1 = code_dict['email']
        str2 = current_app.config['REGISER_CODE']
        str3 = code_dict['password']

        src = str1 + str2 + str3

        m = md5()
        m.update(src.encode('utf-8'))

        if code_dict['register_key'] != m.hexdigest():
            raise PetLog_DataError(
                'Error : One other person post register interface')
        else:
            return True

class verify_email(Resource):
    @checke_interface
    def post(self):
        email = request.json['email']
        if not email.strip():
            return jsonify(status=0,
                        message = "failed")

        code = ''.join(random.sample([chr(i) for i in range(65,91)] + 
                                    [chr(i) for i in range(48,58)],5))
        send_registered_email(email,code)
        
        m = md5()
        m.update(code.encode('utf-8'))

        return jsonify(status=1,
                    code=m.hexdigest())

class user_avatar(Resource):
    @checke_interface
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
            m.update((str1 + str2).encode ('utf-8'))

            filename = str(m.hexdigest()) + str3

            file.save (os.path.join(
                current_app.config['USER_AVATAR_FOLDER'],
                filename))
            
            #文件上传成功，返回文件名
            return jsonify(status = 1,\
                    filename = filename)
        else:
            return jsonify(status = 0,\
                        message = "failed")