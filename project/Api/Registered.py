from flask_restful import Resource
from flask import jsonify,request, current_app
from project.models import User, PetShow_DataError
from project.extra import send_email, checke_interface
from hashlib import md5

class registered(Resource):
    @checke_interface
    def post(self):
        if self.verify_code(request.json):
            user = User()
            user_dict = user.verify_data(request.json,verify_type = 'register')
            user.create_user(user_dict)
            user.insert()

            #用于调试查看的
            print ("phonenumber:%s,user_nickname:%s,password:%s"  %  (\
                user_dict['phonenumber'],
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
                raise PetShow_DataError('Error : One other person post register interface')
        except PetShow_DataError as error:
            print(error.message)
            raise PetShow_DataError
        except KeyError as error:
            print("KeyError : Don't has " + error)
            raise KeyError
        except:
            return False
        else:
            return True

class verify_code(Resource):
    @checke_interface
    def post(self):
        email = request.json['email']
        if not email.strip():
            return jsonify(status=0,
                        message = "failed")

        send_email(email)
        return jsonify(status=1,
                    message="success")
