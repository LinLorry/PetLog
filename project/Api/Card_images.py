from project.extra import login_required,checke_interface, allowed_file
from flask_restful import Resource
from flask import request, current_app, g, jsonify, Response
from werkzeug import secure_filename
import os

# 上传文件的限制格式
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg'])

# 限制上传文件的格式函数

class upload_card_image(Resource):
    #上传卡片图像的类
    @login_required
    def post(self):
        file = request.files['image']
        if file and allowed_file(file.filename):
            #str1是用户的id
            #str2是用户发布的图片数
            #str3是图片的后缀
            str1 = g.user.get_user_id()
            str2 = g.user.get_image_number()
            str3 = '.' + file.filename.rsplit('.')[1]

            filename = str1 + str2 + str3 

            file.save (os.path.join(
                current_app.config['CARD_IMAGES_FOLDER'],
                filename))
        else:
            return jsonify(status = 0,\
                        message = "failed")

        #文件上传成功，返回文件名
        return jsonify(status = 1,\
                    filename = filename)

class download_card_image(Resource):
    @checke_interface
    def get(self, filename):
        if allowed_file(filename):
            image = open(os.path.join(current_app.config['CARD_IMAGES_FOLDER'],
                                      filename))
            resp = Response(image, mimetype="image/jpeg")
            return resp
        else:
            return jsonify(status=0,
                           message='failed')
