from flask_restful import Resource
from flask import jsonify,request
from project.models import User
from project.extra import send_email

class registered(Resource):
    def post(self):
        try:
            user_dict = request.json
            
            user_dict['phonenumber']
            user_dict['user_nickname']
            user_dict['password']

            if not (user_dict['phonenumber'].strip() or \
                user_dict['email'].strip()) or \
                not user_dict['user_nickname'].strip() or \
                not user_dict['password'].strip():
                
                return jsonify(status = 0,message = "error!!")

        except KeyError:
            return jsonify(status = 0,message = "error!!please don't try to do someting wrong")
        except AttributeError:
            return jsonify(status = 0,message = "error!!please don't try to do someting wrong")
        except:
            return jsonify(status = 0,message = "look like something wrong happen")

        #用于调试查看的
        print ("phonenumber:%s,user_nickname:%s,password:%s"  %  (\
                user_dict['phonenumber'],
                user_dict['user_nickname'],
                user_dict['password'])  )

        try:
            user = User()
            user.create_user(user_dict)
        except:
            return jsonify(status = 0,message = "look like something wrong happen")

        
        return jsonify(status = 1, message = "success")

class verify_code(Resource):
    def post(self):
        try:
            email = request.json['email']
            if not email.strip():
                return jsonify(status = 0,message = "error!!please don't try to do someting wrong")
        except:
            return jsonify(status = 0,message = "error!!please don't try to do someting wrong")
        
        send_email(email)
        return jsonify(status = 1,message = "success")
