from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app,g

#用户模块
class User:
    #tablename is 'users'
    __tablename__ = 'users'
    #user_id is 16 characters
    __user_id = '123456789ABCDEF'
    __image_number = 0
        
    def __init__(self,username):
        self.__user_name = username
        self.password = username

    #为password加上修饰器@property
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = pwd_context.encrypt(password)
    
    #校验密码方法
    def verify_password(self, password):
        return pwd_context.verify(password,self.password_hash)
    
    #返回用户的名字的方法
    def get_user_name (self):
        return self.__user_name

    #返回用户id的方法
    def get_user_id (self):
        return self.__user_id
    
    #获取用户上传图片数的方法
    def get_image_number(self):
        return self.__image_number
    
    #获取token的方法，默认时间是10分钟(10*60秒)
    def generate_auth_token(self, expiration = 600):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in = expiration)
        return s.dumps({ 'id': self.get_user_id() ,\
                        'username':self.get_user_name()})

    #插入卡片数据的方法
    def create_card(self,card_dict):

        str1 = g.user.get_user_name()
        str2 = card_dict['time']
        ss = str1 + str2
        card_id = pwd_context.encrypt(ss)[8:-8]

        #插入卡片数据
        return "success"

    def create_user(self,user_dict):

        str1 = user_dict['username']
        str2 = user_dict['joined_time']
        ss = str1 + str2
        self.__user_id = pwd_context.encrypt(ss)[8:-8]
        password = user_dict['password']

        return True