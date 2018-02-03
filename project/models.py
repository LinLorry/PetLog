
import pymysql
pymysql.install_as_MySQLdb()


from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import random
import time
from datetime import datetime
import uuid
from . import db
from flask import current_app,g

''' #使用session进行数据库操作
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#db ?= engine
engine= create_engine('mysql://username:password@localhost/')
Session = sessionmaker(bind=engine)
session = Session() '''

#用户模块
#现在先优先完成用户的注册方法和卡片的创造方法
class User(db.Model):
    #tablename is 'users'
    __tablename__ = 'users'
    #限制变量的访问，加"__"
    __id = db.Column(db.String(16),primary_key=True,nullable=False)
    __user_nickname = db.Column(db.String(20),unique=True,nullable=False)
    __password_hash = db.Column(db.String(128),nullable=False)
    __phonenumber = db.Column(db.String(11),unique=True,nullable=False)
    __gender = db.Column(db.String(1),nullable=True)
    __avatar_path = db.Column(db.String(128),nullable=True)
    __motto = db.Column(db.String(256),nullable=True)
    __address = db.Column(db.String(30),nullable=True)
    __joined_time = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
    __grade = db.Column(db.Integer,nullable=False,default=1)

    #构造函数
    #接口使用的时候要通过这个确定用户
    #information_dict是查找用户提供的信息字典
    #create_dict是创造用户提供的信息字典
    def __init__(self,information_dict = None,create_dict = None):
        if create_dict:
            #生产用户的唯一id
            self.__id = uuid.uuid1()

            #对于必须拥有的变量调用赋值即可
            self.__phonenumber = create_dict['phonenumber']
            self.__user_nickname = create_dict['user_nickname']
            self.password = create_dict['password']
        
            #对于不一定拥有的变量调用set设置器
            #有些设置器还未写,需要补充
            self.set_user_gender(create_dict['gender'])
            self.set_motto(create_dict['motto'])
            #......
        else:
            self.__user_name = information_dict['username']
            #这个是为了测试，所以将密码设置的和用户名一样
            self.password = information_dict['username']

        #根据username 或者 id 初始化一个用户对象......
 
    #为password加上修饰器@property
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    #稍微修改了密码的hash算法
    #密码hash用"密码+用户名+salt"的方法来算
    @password.setter
    def password(self,password):
        self.__password_hash = pwd_context.encrypt(password + \
                                            self.__user_name + \
                                            current_app.config['SALT'])
    
    #校验密码方法
    def verify_password(self, password):
        return pwd_context.verify(password + \
                                self.__user_name + \
                                current_app.config['SALT'],\
                                self.__password_hash)
    
    #返回用户的名字的方法
    def get_user_name (self):
        return self.__user_name

    #返回用户id的方法
    def get_user_id (self):
        return self.__user_id

    #设置用户的性别的方法
    #查看字典是否有该属性
    def set_user_gender (self,user_gender):
        if user_gender == '':
            self.__gender = None
        else:
            self.__gender = user_gender
        return True

    #设置用户的电话号码
    def set_motto (self,user_motto):
        if user_motto == '':
            self.__motto = None
        else:
            self.__motto = user_motto
        return True
            
    #获取token的方法，默认时间是10分钟(10*60秒)
    #密钥使用配置属性，配置属性来自系统变量在project.__init__.py里
    #加上用户名好在检查token结束后，构造用户对象
    def generate_auth_token(self, expiration = 600):
        s = Serializer(current_app.config['SECRET_KEY'],\
                    expires_in = expiration)
        return s.dumps({ 'id': self.__id ,\
                        'username':self.__user_name})

    #用户创造卡片的方法
    def create_card(self,create_dict):
        #创造卡片对象
        create_dict['user_id'] = self
        card = Card(create_dict=create_dict)
        card.insert()

        return True

    def create_pet(self,create_pet):
        create_pet['user_id'] = self
        pet = Pet(create_dict = create_pet)
        #pet.insert()

        return True

    #计算用户当前等级的方法
    def grade_now(self,grade,user_id,comment_number,praise_number):
	    #具体计算待定
	    return grade

class Card():
    __tablename__ = "cards"
    #卡片
    #还没完善,插入的方法还没有......
	
    ''' __id = db.Column()
    __content = db.Column()
    __time = db.Column()
    __images = db.Column() '''

    ''' user_id = db.Column() '''

    #用于用户查找他的卡片的方法
    def __init__(self,card_dict = None,create_dict = None):
        #这块搞错了，
        ''' #这里应该是用用户名去查找表中的user_id ，然后再赋值给user_id~
        the_id = session.query(User.user_id).filter_by(user_name=user_name)
        self.__user_id = the_id '''
        if create_dict:
            self.__id = uuid.uuid1()
            self.__content = create_dict['content']
            self.__images = create_dict['images']
            self.__tags = create_dict['tags']
            #self.__user_id = create_dict['user_id']                    
        else:
            #这块是按照卡片id查找卡片并初始化一个卡片对象的方法
            pass

    def insert(self):
        #内容记录进数据库
        db.session.add(self)
        db.session.commint()
        #session.close()

class Pet():
    #宠物

    #宠物的构造函数，用于查找一个宠物
    def __init__(self,pet_dict = None,create_dict = None):
        if create_dict:
            #宠物唯一id的生成
            self.__pet_id = uuid.uuid1()
            self.__category = create_dict['category']
            self.__pet_name = create_dict['pet_name']
            self.__user_id = create_dict['user_id']
            self.__gender = create_dict['gender']
        elif pet_dict['user_phonenumber']:
            pass
        else:
            pass

    def insert(self):
        #内容记录进数据库
        db.session.add(self)
        db.session.commint()
        #session.close()
                