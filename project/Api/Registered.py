import os
import random
from flask_restful import Resource
from flask import jsonify,request, current_app
from project.Models.User import User
from project.Models.PetLogDataError import PetLog_DataError
from project.extra import send_email, checke_interface, allowed_file
from hashlib import md5
from werkzeug import secure_filename

class registered(Resource):
    @checke_interface
    def post(self):
        if self.verify_code(request.json):
            user = User("user")
            user_dict = user.verify_data(request.json,verify_type = 'register')
            user.create_user(user_dict)
            self.change_image_name(request.json['image'],
                                    user.get_user_id)
            user.insert()

            #用于调试查看的
            print ("email:%s,user_nickname:%s,password:%s"  %  (\
                user_dict['email'],
                user_dict['user_nickname'],
                user_dict['password']))

            return jsonify(status=1,
                        message="success")
        else:
            return jsonify(status=0,
                        message='failed')

    def change_image_name(self,image_name,user_id):
        if os.path.exists(
                os.path.join(
                    current_app.config['USERHEAD_IMAGES_FOLDER'],
                    image_name)):
            os.rename(os.path.join(
                    current_app.config['USERHEAD_IMAGES_FOLDER'],
                    image_name),
                    os.path.join(
                    current_app.config['USERHEAD_IMAGES_FOLDER'],
                    user_id + '.' + image_name.rsplit('.')[1]))
        else:
            pass
        return True

    def verify_code(self, code_dict):
        try:
            str1 = code_dict['email']
            str2 = current_app.config['REGISER_KEY']
            str3 = code_dict['password']

            src = str1 + str2 + str3
            m = md5()
            m.update(src.encode('utf-8'))
            if code_dict['code'] != m.hexdigest():
                raise PetLog_DataError(
                    'Error : One other person post register interface')
        except PetLog_DataError as error:
            print(error.message)
            raise PetLog_DataError
        except KeyError as error:
            print("KeyError : Don't has " + str(error))
            raise KeyError
        except:
            return False
        else:
            return True

class verify_email(Resource):
    @checke_interface
    def post(self):
        email = request.json['email']
        code = ''.join(random.sample([chr(i) for i in range(65,91)],5))
        if not email.strip():
            return jsonify(status=0,
                        message = "failed")

        send_email(email,code)
        m = md5()
        m.update(code.encode('utf-8'))
        return jsonify(status=1,
                    code=m.hexdigest())

class new_user_image(Resource):
    @checke_interface
    def post(self):
        file = request.files['image']
        if file and allowed_file(file.filename):
            #str1是用户的id
            #str2是图片的后缀
            str1 = secure_filename(file.filename)
            str2 = '.' + file.filename.rsplit('.')[1]

            filename = str1 + str2

            file.save (os.path.join(
                current_app.config['USERHEAD_IMAGES_FOLDER'],
                filename))
            
            #文件上传成功，返回文件名
            return jsonify(status = 1,\
                    filename = filename)
        else:
            return jsonify(status = 0,\
                        message = "failed")