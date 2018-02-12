import pymysql
pymysql.install_as_MySQLdb()

from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import random
import time
from datetime import datetime
import uuid
from . import db
from flask import current_app, g

# 用户模块

class User(db.Model):
    __tablename__ = "users"
    __id = db.Column(db.String(16), primary_key=True, nullable=False)
    __user_nickname = db.Column(db.String(20), unique=True, nullable=False)
    __password_hash = db.Column(db.String(128), nullable=False)
    __phonenumber = db.Column(db.String(11), unique=True, nullable=False)
    __gender = db.Column(db.String(1), nullable=True)
    __avatar_path = db.Column(db.String(128), nullable=True)
    __motto = db.Column(db.String(256), nullable=True)
    __address = db.Column(db.String(30), nullable=True)
    __joined_time = db.Column(db.DateTime, nullable=False)
    __grade = db.Column(db.Integer, nullable=False)
    __email = db.Column(db.String(32), nullable=False)

    # 构造函数
    # 接口使用的时候要通过这个确定用户
    # information_dict是查找用户提供的信息字典
    # create_dict是创造用户提供的信息字典

    def verify_data(self, data_dict, verify_type):
        try:

            if verify_type == "register":
                # 用户必须有邮箱，昵称和密码
                if not data_dict['email'] or \
                        not data_dict['user_nickname'] or \
                        not data_dict['password']:
                    raise PetShow_DataError("Error : One register lack something")
            elif verify_type == "create_card":
                # 内容和图片不能同时没有
                if not (data_dict['content'] or
                        data_dict['images']) or \
                    not data_dict['time']:
                    raise PetShow_DataError("Error : One post card lack something")
                else:
                    data_dict['time'] = int(data_dict['time']) * (10 ** -3)
            elif verify_type == "auth":
                #验证登陆一定有邮箱和密码
                if not data_dict['email'] or \
                    not data_dict['password']:
                    raise PetShow_DataError("Error : One login lack something")

        except KeyError as error:
            print("KeyError : Don't has " + error)
            raise KeyError

        except PetShow_DataError as e:
            print(e.message)
            raise PetShow_DataError

        else:
            return data_dict
    #----------------->生成用户的方法
    #------>用户注册
    #上面的方法和这个是一样的用处的

    def checke_create(self, create_dict):
        if (create_dict['phonenumber'] is None) or (create_dict['user_nickname'] is None) or (create_dict['password']is None) or (create_dict['email'] is None):
            return "您的信息录入不完全，请检查"
        else:
            if len(create_dict['phonenumber']) != 11:
                return "电话号码格式不正确"
            else:
                if create_dict['password'] != create_dict['password1']:
                    return "您两次输入的密码不一致"
                else:
                    return create_dict

    def create_user(self, create_dict):

        # create_dict(必须）要传来的数据有：手机号码（不可重复），昵称（可重复），密码，注册的时间，验证的邮箱的号码。
        '''{'phonenumber':'12345678911',
        'user_nickname':'who are you',
        'password':'90909090',
        'password1':'90909090',
        'jioned_time':'20170909',
        'email':'117676868@qq.com',
        'grade':'1'
        # 下面的为不一定填的
        'address':'江西上饶'，
        'motto':'我没什么好说的',
        'avatar':'dizhi',
        'gender':'你猜',
        }'''

        # 生产用户的唯一id
        self.__id = uuid.uuid1()

        # 对于必须拥有的变量调用赋值即可
        self.__phonenumber = create_dict['phonenumber']
        self.__user_nickname = create_dict['user_nickname']
        self.password = create_dict['password']
        self.__joined_time = create_dict['joined_time']
        self.__email = create_dict['email']

        self.__grade = 1  # 直接赋值，初始用户等级均为1
        self.__avatar_path = touxiangweizhi  # 直接赋值，后端存储一张为默认头像

        # 对于不一定拥有的变量调用set设置器（由后端自动生成字段）
        # 有些设置器还未写,需要补充(若为空赋值为后面的结果)

        self.set_address(create_dict['address'])  # 设置为未知
        self.set_user_gender(create_dict['gender'])  # 设置为空
        self.set_motto(create_dict['motto'])  # 设置为此用户暂无简介

    # 设置用户的性别的方法
    # 查看字典是否有该属性
    def set_address(self, user_address):
        if user_address == '':
            self.__address = '未知'
        else:
            sefl.__address = user_address

    def set_user_gender(self, user_gender):
        if user_gender == '':
            self.__gender = '空'
        else:
            self.__gender = user_gender
        return True

    def set_motto(self, user_motto):
        if user_motto == '':
            self.__motto = '此用户暂无简介。'
        else:
            self.__motto = user_motto
        return True

    #同下面这个一样写一个更新的方法update()

    def insert(self):
        db.session.add(self)
        db.session.commit()
    #------****我不大清楚。。
    #这是查询用户的方法，下面的是我为了测试方便写的，可以不用理

    def select(self, user_dict):
        # 调试用
        self.__id = user_dict['email']
        self.__email = user_dict['email']
        self.__user_nickname = user_dict['email']
        self.password = user_dict['email']

    #------> 登陆时检验密码是否正确
    #谔谔，这段emmmm其实不需要的
    def login_check(self, login_dict):
        '''示例：
        login_dict{'phonenumber':'53458745467',
                   'password':'767678222'}'''
        #-------------------------
        #这里是email吧
        #someone = login_dict['phonenumber']


        someone = login_dict['eamil']
        someone_key = login_dict['password']
        user = self.query.filter_by(__phonenumber=someone).first()
        if user is None:
            return '此账号尚未注册'
        else:
            if user.verify_password(someone_key):
                g.user = self.query.filter_by(__phonenumber=someone).first()
                token = g.user.generate_auth_token()
                return {'massage': 'true', 'token': token}
            else:
                return {'massage': 'flase'}
    #------------------------>查找用户的方法(通过昵称搜索用户)

    def find_all_user_number(self, nickname):  # 传入要找的用户的昵称
        peoples = self.query.filter_by(__user_nickname=nickname).all()
        number = len(peoples)
        return number  # 返回的为同一昵称的用户的总数

    def find_all_user(self, nickname):  # 传入要找的用户的昵称
        peoples = self.query.filter_by(__user_nickname=nickname).all()
        users = []
        for people in peoples:
            users.append({'nickname': people.__user_nickname,
                          'avatar': people.__avatar_path,
                          'joined_time': people.__joined_time})
        return users  # 由于名称可重复，返回的为同一昵称的用户的id列表

    #--------->(查询自身信息,查询某人的详细信息）
    #像这样的方法需要写多几个，不单是靠id查找，还有email查找等等
    #这类的方法名可以是find_user_XXX(XXX是查找条件),这类查找是精确查找的，有可能有多个条件
    def find_user(self, user_id):  # 传入某一用户的id 返回的是某人的详细信息
        info = self.query.filter_by(__id=user_id).first()
        information = {'nickname': info.__user_nickname,
                       'phonenumber': info.__phonenumber,
                       'gender': info.__gender,
                       'avatar': info.__avatar_path,
                       'motto': info.__motto,
                       'address': info.__address,
                       'grade': info.__grade}
        return infomation  # 传出此人详细的信息

    #---------------------->更改用户信息的方法
    '''update_dict 为修改后的所有信息形成的字典（包含所有可以后期改动的数据信息，无论是否有改动，均重新赋值）
    update_dict{'user': '2367821367'
                'new_gender': '你继续猜',
                'new_avatar': 'hiohoh',
                'new_motto': '我没什么好说的，怎么还没完成',
                'new_address': '江西上饶'}'''

    def update_user(self,update_dict):
        it = self.query.filter_by(__id=update_dict['user']).first()
        it.__gender = update_dict['new_gender']
        it.__avatar_path = update_dict['new_avatar']
        it.__motto = update_dict['new_motto']
        it.__address = update_dict['new_address']

    #---------------------->用户的操作部分
    #-------------------->用户的卡片部分的操作
    #-------->发布动态

    def create_card(self, card_dict):
        card = Card()
        card_dict
        card.create_card(card_dict)
        return True

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # 稍微修改了密码的hash算法
    # 密码hash用"密码+用户名+salt"的方法来算
    @password.setter
    def password(self, password):
        self.__password_hash = pwd_context.encrypt(password +
                                                   current_app.config['SALT'] +
                                                   self.__id)

    # 校验密码方法
    def verify_password(self, password):
        return pwd_context.verify(password +
                                current_app.config['SALT'] +
                                self.__id,
                                  self.__password_hash)

    # 返回用户的名字的方法
    def get_user_name(self):
        return self.__user_name

    # 返回用户id的方法
    def get_user_id(self):
        return self.__user_id

    # 获取token的方法，默认时间是10分钟(10*60秒)
    # 密钥使用配置属性，配置属性来自系统变量在project.__init__.py里
    # 加上用户名好在检查token结束后，构造用户对象
    def generate_auth_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.__id,
                        'email': self.__email})

    # 计算用户当前等级的方法
    def grade_now(self, grade, user_id, comment_number, praise_number):
            # 具体计算待定
        return grade

class Card(db.Model):
    """card model"""
    __tablename__ = "cards"
    __id = db.Column(db.String(16), primary_key=True, nullable=False)
    __user_id = db.Column(db.String(16), nullable=False)
    __pet_id = db.Column(db.String(16), nullable=False)
    __card_content = db.Column(db.Text, nullable=True)
    __card_image_path = db.Column(db.String(128), nullable=True)
    __card_time = db.Column(db.DateTime, nullable=False)

    #------>发布动态

    def create_card(self, create_dict):
        # 创造卡片对象
        '''create_dict必须带有的信息为：发布者的id,发布的内容（内容不得为空），相关的宠物的id,图片可以为空，标签不得为空。
        例如（仅是必须包括的信息的示例）：（标签不得为空，便于为卡片分类）
        {
            'content':'iihoi'，
            'petname':'奥利奥'，
            'pet_id':'989078989'，
            'user_id':'26372832673678',
            'tags':{"1","2"}
        }

        '''
        self.__id = uuid.uuid1()
        self.__user_id = create_dict['user_id']
        self.__content = create_dict['content']
        self.__pet_id = create_dict['pet_id']

        # 以下部分为发布卡片不一样要携带的信息
        self.__images = ['images']
        self.__tags = create_dict['tags']
        pass

    def set_card_image(self, card_image):
        pass

    def insert(self):
        # 内容记录进数据库
        db.session.add(self)
        db.session.commint()
        # session.close()
        return True

    def time_card(self, user_id):
        that = user_all_pet(user_id)
        num = len(that)
        for i in range(len(that)):
            pet = that[i]['id']
            cards = self.query.filter_by(__pet_id=pet).all()
            # 找到所有该宠物的卡片
            # 之后按照时间排序，分组，返回以一个月为一组的数据。


class Pet(db.Model):  # 待补充，宠物头像，以及宠物的介绍
    __tablename__ = "pets"
    __pet_id = db.Column(db.String(16), nullable=False, primary_key=True)
    __category = db.Column(db.String(32), nullable=False)
    __detailed_category = db.Column(db.String(64), nullable=True)
    __pet_name = db.Column(db.String(20), nullable=False)
    __user_id = db.Column(db.String(16), nullable=False)
    __time = db.Column(db.DateTime, nullable=False)
    __gender = db.Column(db.String(1), nullable=False)
    __pet_avatar_path = db.Column(db.String(128), nullable=False)

    # 宠物的构造函数，用于查找一个宠物
    def __init__(self, pet_dict=None, create_dict=None):
        pass

    def create_pet(self, create_dict):
        # 宠物唯一id的生成
        self.__pet_id = uuid.uuid1()
        self.__category = create_dict['category']
        self.__pet_name = create_dict['pet_name']
        self.__user_id = create_dict['user_id']
        self .__gender = create_dict['gender']
        pass

    def insert(self):
        # 内容记录进数据库
        db.session.add(self)
        db.session.commint()
        # session.close()

    def user_all_pet(self, user_id):
        # 时间轴界面下获取某用户所有宠物的id
        pets = self.query.filter_by(__user_id=user_id).all()
        all_pet = []
        for pet in pets:
            all_pet.append({'id': pet.__pet_id, 'name': pet.__pet_name})
        return all_pet
        # 返回某用户所有的宠物id（以列表套字典的格式返回）例：[{'id':'08980','name':'奥利奥'},{'id':'87389','name':'趣多多'}]
        # 时间轴界面会显示的有关宠物方面的信息（待补充）

#----->评论方面


class Comment(db.Model):
    __tablename__ = "comments"
    __id = db.Column(db.String(16),primary_key=True, nullable=False)
    __card_id = db.Column(db.String(16), nullable=False)
    __user_id = db.Column(db.String(16), nullable=False)
    __to_user_id = db.Column(db.String(16), nullable=False)
    __comment_content = db.Column(db.Text, nullable=False)

    def comment_on_card(self, comment_card_dict):
        '''示例：newcomment_dict{'card_id':'67687',
                                'user_id':'787897',
                                'to_user_id':'79980980',
                                'commtent_content':'真的有点很烦呢。'}'''
        self.__id = uuid.uuid1()
        self.__card_id = card_id
        self.__user_id = user_id
        self.__to_user_id = to_user_id
        self.__comment_content = comment_content

class Praise(db.Model):
    __tablename__ = "praise"
    __id = db.Column(db.String(16),primary_key=True, nullable=False)
    def create_praise(self,card_id,user_id):
        pass
    def del_praise(self,card_id,user_id):
        pass

class Follow(db.Model):
    __tablename__ = "follow"
    __id = db.Column(db.String(16),primary_key=True, nullable=False)
    def create_follow(self,user_id,be_concerned_id):
        pass
    
    def del_follow(self,user_id,be_concerned_id):
        pass

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

class PetShow_DataError(Exception):
    def __init__(self,message):
        Exception.__init__(self)
        self.message = message

