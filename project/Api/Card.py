from flask_restful import Resource
from project.extra import login_required
from project.models import User
from flask import request,g,jsonify

class post_card(Resource):
    #发布动态接口

    @login_required
    def post(self):
        card_dict = request.json

        try:
            card_dict['content']
            card_dict['images']

            #内容和图片不能同时没有
            if not (card_dict['content'].strip() or \
                    card_dict['images'].strip()):
                return jsonify(status = 0,\
                message = "content and image can't exist at the same time.")
        
        except KeyError:
            return jsonify(status = 0,message = "error!!please don't try to do someting wrong")
        except AttributeError:
            return jsonify(status = 0,message = "error!!please don't try to do someting wrong")        
        except:
            return jsonify(status = 0,message = "look like something wrong happen")

        #用于调试查看的
        print ("content:%s,images:" % \
            (card_dict['content']),\
            card_dict['images'])

        try:      
            g.user.create_card(card_dict)
        except:
            return jsonify(status = 0,message = "look like something wrong happen")

        return jsonify(status = 1,\
                message = "success")

class user_get_card(Resource):
    #用户自己的动态获取接口

    @login_required
    def post(self):
        return jsonify(status = 1,\
                message = "success")

class guest_get_card(Resource):
    #访客随机获取的动态接口

    def post(self):
        return jsonify(status = 1,\
                message = "success")
