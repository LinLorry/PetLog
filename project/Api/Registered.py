from flask_restful import Resource
from flask import jsonify,request
from project.models import User

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
            user = User(create_dict = user_dict)
        except:
            return jsonify(status = 0,message = "look like something wrong happen")

        
        return jsonify(status = 1, message = "success")