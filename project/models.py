from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import random
import time
import hashlib

#用户模块
class User(db.Model):
    #tablename is 'users'
    __tablename__ = 'users'
    _id = db.Column(db.String(16),primary_key=True,nullable=False)
    user_name = db.Column(db.String(20),unique=True,nullable=False)
    user_nickname = db.Column(db.String(20),unique=True,nullable=False)
    password_hash = db.Column(db.String(128),nullable=False)
    phonenumber = db.Column(db.String(11),unique=True,nullable=False)
    gender = db.Column(db.String(1),nullable=True)
    head_portrait_path = db.Column(db.String(128),nullable=True)
    motto = db.Column(db.String(256),nullable=True)
    address = db.Column(db.String(30),nullable=True)
    joined_time = db.Column(db.Datetime,nullable=False,default=datetime.now)
    grade = db.Column(db.Integer,nullable=False,default=1)

    #user_id is 16 characters
#    __user_id = '123456789ABCDEF'

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

    #添加该用户宠物信息的方法
    def create_pet(user_id):
	
	str1 = user._id
	str2 = time.time()
	str3 = "new pet"
	str4 = str1+str(str2)+str3
	raw = hashlib.md5()
	raw.update(str4.encode("utf8"))
	result = raw.hexdigest()[8:-8]
	return result

    #添加新用户时生成id的方法
    def create_user(user_name):

	str1 = user_name
    str2 = time.time()
	str3 = "new people"
    str4 = str1+str(str2)+str3
	raw = hashlib.md5()
	raw.update(str4.encode("utf8"))
	result = raw.hexdigest()[8:-8]
	return result

    #某用户发出卡片时生成id的方法
    def create_card(user_id):
	
	str1 = user_id
    str2 = time.time()
	str3 = "new card"
	str4 = str1+str(str2)+str3
	raw = hashlib.md5()
	raw.update(str4.encode("utf8")
	result = raw.hexdigest()[8:-8]
	return result

    #计算用户当前等级的方法
    def grade_now(grade,user_id,comment_number,praise_number)
	#具体计算待定
	return grade

    #
