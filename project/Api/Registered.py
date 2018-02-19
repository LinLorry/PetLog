import random
from flask_restful import Resource
from flask import jsonify,request, current_app
from project.Models.User import User
from project.Models.PetLogDataError import PetLog_DataError
from project.extra import send_email, checke_interface
from hashlib import md5

class registered(Resource):
    @checke_interface
    def post(self):
        if self.verify_code(request.json):
            user = User("user")
            user_dict = user.verify_data(request.json,verify_type = 'register')
            user.create_user(user_dict)
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

    def verify_code(self, code_dict):
        try:
            str1 = code_dict['email']
            str2 = current_app.config['REGISER_KEY']
            str3 = code_dict['password']

            src = str1 + str2 + str3
            m = md5()
            m.update(src.encode('utf-8'))
            if code_dict['code'] != m.hexdigest():
                raise PetLog_DataError('Error : One other person post register interface')
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
