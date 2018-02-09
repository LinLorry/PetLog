from flask_restful import Resource
from flask import jsonify,request,current_app
from project.models import User
from project.extra import send_email
import md5

class registered(Resource):
    def post(self):
        try:
            self.verify_code(request.json)
            user = User()
            user_dict = user.verify_data(request.json)
            user.create_user(user_dict)
            user.insert()

            #用于调试查看的
            print ("phonenumber:%s,user_nickname:%s,password:%s"  %  (\
                user_dict['phonenumber'],
                user_dict['user_nickname'],
                user_dict['password'])  )
        except:
            return jsonify(status =0, \
                    message = "failed")
        else:
            return jsonify(status = 1, message = "success")

    def verify_code(self,code_dict):
        try:
            str1 = code_dict['email']
            str2 = current_app.config['REGISER_KEY']
            str3 = code_dict['password']

            src = str1 + str2 + str3
            m = md5.new()
            m.update(src)
            if code_dict['code'] != m.hexdigest():
                raise KeyError
            else:
                return True
        except:
            raise KeyError

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
