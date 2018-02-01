from flask_restful import Resource
from flask import jsonify.request
from project.models import User

class registered(Resource):
    def post(self):
        try:
            user_dict = request.json
            
            user_dict['username']
            user_dict['user_nickname']
            user_dict['password']
            
            user = User(user_dict) 
        except KeyError:
            jsonify(status = 0,message = "error!!please don't try to do someting wrong")
        except:
            jsonify(status = 0,message = "look like something wrong happen")
        
        #用于调试查看的
        print ("username:%s,user_nickname:%s,password:%s"  %  (\
                user_dict['username'],
                user_dict['user_nickname'],
                user_dict['password'])  )
        
        return jsonify(status = 1, message = 1)