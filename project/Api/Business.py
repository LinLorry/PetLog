import re
from flask import jsonify, g, request
from flask_restful import Resource
from project.models import Follow,User
from project.extra import login_required, checke_interface

class follow_interface(Resource):
    @login_required
    def get(self):
        re_com = re.compile(r'^action\=(\d)\&lastCursor\=\$(.*)$')
        r = re_com.match(request.query_string.decode('utf-8'))

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
        return jsonify(user_information = g.user.get_information()) 

class user_other_information(Resource):
    @login_required
    def post(self):
        return jsonify(user_information = \
                        g.user.get_other_information(
                            request.json['user_id']))

class guest_get_information(Resource):
    @checke_interface
    def post(self):
        user = User("guest")
        return jsonify(user_information = \
                        user.get_other_information(
                            request.json['user_id']))

# 上传文件的限制格式
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg'])

# 限制上传文件的格式函数
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in \
           ALLOWED_EXTENSIONS

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
    #@login_required
    def get(self, filename):
        if allowed_file(filename):
            image = open(os.path.join(current_app.config['CARD_IMAGES_FOLDER'],
                                      filename))
            resp = Response(image, mimetype="image/jpeg")
            return resp
        else:
            return jsonify(status=0,
                           message='failed')

