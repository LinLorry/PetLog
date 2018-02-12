from project.extra import login_required,checke_interface
from flask_restful import Resource
from flask import request,current_app,g,jsonify
from werkzeug import secure_filename
import os

class upload_card_images(Resource):
    #上传卡片图像的类

    #上传文件的限制格式
    __ALLOWED_EXTENSIONS = set (['jpg','png','jpeg'])

    #限制上传文件的格式函数
    def allowed_file(self,filename):
        return '.' in filename and \
            filename.rsplit('.',1)[1] in \
                self.__ALLOWED_EXTENSIONS
    
    @login_required
    def post(self):
        file = request.files['image']
        if file and self.allowed_file(file.filename):
            #str1是用户的id
            #str2是用户发布的图片数
            #str3是图片的后缀
            str1 = g.user.get_user_id()
            str2 = g.user.get_image_number()
            str3 = '.' + file.filename.rsplit('.')[1]

            filename = str1 + str2 + str3 

            file.save (os.path.join(\
                current_app.config['CARD_IMAGES_FOLDER'],\
                filename))
        #没有文件或文件格式不是允许的文件格式，返回"f",失败
        else:
            return jsonify(status = 0,\
                        message = "failed")

        #文件上传成功，返回文件名
        return jsonify(status = 1,\
                    filename = filename)

class download_card_images(Resource):
    @login_required
    def post(self):
        return "ss"
