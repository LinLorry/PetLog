
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
    __tablename__ = "users"
    __id = db.Column(db.String(16),primary_key=True,nullable=False)
    __user_nickname = db.Column(db.String(20),unique=True,nullable=False)
    __password_hash = db.Column(db.String(128),nullable=False)
    __phonenumber = db.Column(db.String(11),unique=True,nullable=False)
    __gender = db.Column(db.String(1),nullable=True)
    __avatar_path = db.Column(db.String(128),nullable=True)
    __motto = db.Column(db.String(256),nullable=True)
    __address = db.Column(db.String(30),nullable=True)
    __joined_time = db.Column(db.DateTime,nullable=False)
    __grade = db.Column(db.Integer,nullable=False,default=1)
    #构造函数
    #接口使用的时候要通过这个确定用户
    #information_dict是查找用户提供的信息字典
    #create_dict是创造用户提供的信息字典
    def __init__(self,information_dict = None,create_dict = None):
        pass

    def create_user(self,create_dict):
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

    def select(self,user_dict):
        #调试用
        self.__id = user_dict['id']
        self.password = user_dict['id']
        
    def create_card(self,card_dict):
        card = Card()
        card.create_card(card_dict)
        return True

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
                        'phonenumber':self.__phonenumber})

    #计算用户当前等级的方法
    def grade_now(self,grade,user_id,comment_number,praise_number):
	    #具体计算待定
	    return grade

class Card(db.Model):
    """card model"""
    __tablename__ = "cards"
    __id = db.Column(db.String(16),primary_key= True,nullable=False)
    __user_id = db.Column(db.String(16),nullable=False)
    __pet_id = db.Column(db.String(16),nullable=False)
    __card_content = db.Column(db.Text,nullable=True)
    __card_image_path = db.Column(db.String(128),nullable=True)
    __card_time = db.Column(db.DateTime,nullable=False)

    #用于用户查找他的卡片的方法
    def __init__(self,card_dict = None,create_dict = None):
        pass

    def create_card(self,create_dict):
        #创造卡片对象
        self.__id = uuid.uuid1()
        self.__content = create_dict['content']
        self.__images = create_dict['images']
        self.__tags = create_dict['tags']
        pass

    def insert(self):
        #内容记录进数据库
        db.session.add(self)
        db.session.commint()
        #session.close()

class Pet(db.Model):
    __tablename__ = "pets"
    __pet_id = db.Column(db.String(16),nullable=False,primary_key=True)
    __category = db.Column(db.String(32),nullable=False)
    __detailed_category = db.Column(db.String(64),nullable=True)
    __pet_name = db.Column(db.String(20),nullable=False)
    __user_id = db.Column(db.String(16),nullable=False)
    __time = db.Column(db.DateTime,nullable=False)
    __gender = db.Column(db.String(1),nullable=False)

    #宠物的构造函数，用于查找一个宠物
    def __init__(self,pet_dict = None,create_dict = None):
        pass

    def create_pet(self,create_dict):
        #宠物唯一id的生成
        self.__pet_id = uuid.uuid1()
        self.__category = create_dict['category']
        self.__pet_name = create_dict['pet_name']
        self.__user_id = create_dict['user_id']
        self.__gender = create_dict['gender']
        pass

    def insert(self):
        #内容记录进数据库
        db.session.add(self)
        db.session.commint()
        #session.close()
''' 
class Tag(db.Model):
    __tablename__ ="tags"
    __id = db.Column(db.String(16),nullable=False)
    __tag_name = db.Column(db.String(32),nullable=False)

class Card_with_tag(db.Model):
    __tablename__ = "card_with_tag"
    __id = db.Column(db.String(16),nullable=False)
    __card_id = db.Column(db.String(16),nullable=False)
    __tag_id = db.Column(db.String(16),nullable=False) '''

    
                