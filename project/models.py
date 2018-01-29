from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

#用户模块
class User:
    #tablename is 'users'
    __tablename__ = 'users'
    #user_id is 16 characters
    __user_id = '123456789ABCDEF'

    def __init__(self,username):
        self.__user_name = username

    #为password加上修饰器@property
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = pwd_context.encrypt(password)
    
    #校验密码方法
    def verify_password(self, password):
        return pwd_context.verify(self.password_hash, password)
    
    #返回用户的名字的方法
    def get_user_name (self):
        return self.__user_name

    #返回用户id的方法
    def get_user_id (self):
        return self.__user_id
    
    #获取token的方法，默认时间是10分钟(10*60秒)
    def generate_auth_token(self, expiration = 600):
        s = Serializer("ssss",expires_in = expiration)
        return s.dumps({ 'id': self.id })




