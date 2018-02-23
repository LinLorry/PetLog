import uuid
from project import db
from .Pet import Pet
from .Card import Card
from .Praise import Praise
from .Follow import Follow
from .Comment import Comment
from .PetLogDataError import PetLog_DataError
from threading import Thread
from flask import current_app
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(db.Model):
    __tablename__ = "users"
    __id = db.Column(db.String(16), primary_key=True, nullable=False)
    __user_nickname = db.Column(db.String(20), unique=True, nullable=False)
    __password_hash = db.Column(db.String(128), nullable=False)
    __phonenumber = db.Column(db.String(11), unique=True)
    __gender = db.Column(db.String(1), nullable=True)
    __avatar_path = db.Column(db.String(128), nullable=True)
    __motto = db.Column(db.String(256), nullable=True)
    __address = db.Column(db.String(30), nullable=True)
    __joined_time = db.Column(db.DateTime, nullable=False)
    __grade = db.Column(db.Integer, nullable=False)
    __email = db.Column(db.String(32), nullable=False)

    # 构造函数
    #用来构造一个访客的用户对象
    def __init__(self,content=None,option="default"):
        if option == 'id':
            info = self.query.filter_by(__id = content).first()
            self.__id = info.__id
            self.__address = info.__address
            self.__user_nickname = info.__user_nickname
            self.__phonenumber =info.__phonenumber
            self.__gender = info.__gender
            self.__password_hash = info.__password_hash
        elif option == 'default':
            pass
        elif option == 'guest':
            pass

    def verify_data(self, data_dict, verify_type):
        try:

            if verify_type == "register":
                # 用户必须有邮箱，昵称和密码
                if not data_dict['email'] or \
                    not data_dict['user_nickname'] or \
                    not data_dict['password'] or \
                    not data_dict['gender'] or \
                    not data_dict['avatar_path'] or \
                    not data_dict['gender'] :
                    raise PetLog_DataError(
                        "One register lack something")
            elif verify_type == "auth":
                # 验证登陆一定有邮箱和密码
                if not data_dict['email'] or \
                        not data_dict['password']:
                    raise PetLog_DataError(
                        "One login lack something")

        except KeyError as error:
            print("KeyError : Don't has " + error)
            raise KeyError

        except PetLog_DataError as error:
            print("Error : " + error.message)
            raise PetLog_DataError

        else:
            return data_dict

    # ----------------->生成用户的方法
    # ------>用户注册

    def create_user(self, create_dict):

        # create_dict(必须）要传来的数据有：昵称（可重复），密码，#注册的时间，验证的邮箱的号码。
        '''{'user_nickname':'who are you',
        'password':'90909090',
        #'jioned_time':'20170909',
        'email':'117676868@qq.com',
        'grade':'1'
        # 下面的为不一定填的
        'address':'江西上饶'，
        'avatar':'dizhi',
        'gender':'你猜',
        }'''

        # 生产用户的唯一id
        self.__id = str(uuid.uuid1()).split("-")[0]

        # 对于必须拥有的变量调用赋值即可
        self.__email = create_dict['email']
        self.__user_nickname = create_dict['user_nickname']
        self.password = create_dict['password']
        self.__joined_time = datetime.utcnow()#create_dict['joined_time']
        
        self.__grade = 1  # 直接赋值，初始用户等级均为1
        self.__avatar_path = create_dict['avatar_path']

        # 对于不一定拥有的变量调用set设置器（由后端自动生成字段）
        # 有些设置器还未写,需要补充(若为空赋值为后面的结果)

        self.set_address(create_dict['address'])  # 设置为未知
        self.set_user_gender(create_dict['gender'])  # 设置为空
        #self.set_motto(create_dict['motto'])  # 设置为此用户暂无简介
        return True

    # ---------------------------->设置器(set)
    # 设置用户的性别的方法
    # 查看字典是否有该属性

    def set_address(self, user_address):
        if not user_address == '':
            self.__address = user_address
        return True

    def set_user_gender(self, user_gender):
        if not user_gender == '':
            self.__gender = user_gender
        return True

    def set_motto(self, user_motto):
        if not user_motto == '':
            self.__motto = user_motto
        return True

    # ---------------------------->设置器(set)结束

    # ------------------------>查找用户的方法(通过昵称搜索用户)

    def find_all_user_number(self, nickname):  # 传入要找的用户的昵称
        peoples = self.query.filter_by(_User__user_nickname=nickname).all()
        number = len(peoples)
        return number  # 返回的为同一昵称的用户的总数

    def find_all_user(self, nickname):  # 传入要找的用户的昵称
        peoples = self.query.filter_by(_User__user_nickname=nickname).all()
        users = []
        for people in peoples:
            users.append({'nickname': people.__user_nickname,
                          'avatar': people.__avatar_path,
                          'joined_time': people.__joined_time})
        return users  # 由于名称可重复，返回的为同一昵称的用户的id列表

    # --------->(查询自身信息,查询某人的详细信息）
    # 像这样的方法需要写多几个，不单是靠id查找，还有email查找等等 - . -!
    # 只写了id和email两个可以查询出所有详细信息的，当输入昵称时，得到的结果不一定具有唯一性，就不显示全部信息见上面的方法，这方面等与前端的进一步沟通。
    # 这类的方法名可以是find_user_XXX(XXX是查找条件),这类查找是精确查找的，有可能有多个条件

    def find_by_id(self, user_id):  # 传入某一用户的id 返回的是某人的详细信息
        info = self.query.filter_by(_User__id=user_id).first()
        if info is None:
            raise PetLog_DataError("Don't have this id : " + user_id)

        self.__id = info.__id
        self.__user_nickname = info.__user_nickname
        self.__password_hash = info.__password_hash
        self.__gender = info.__gender
        self.__avatar_path = info.__avatar_path
        self.__motto = info.__motto
        self.__address = info.__address
        self.__joined_time = info.__joined_time
        self.__grade = info.__grade
        self.__email = info.__email
        return True

    def find_by_email(self, user_email):
        info = self.query.filter_by(_User__email=user_email).first()
        if info is None:
            raise PetLog_DataError("Don't have this email : " + user_email)

        self.__id = info.__id
        self.__user_nickname = info.__user_nickname
        self.__password_hash = info.__password_hash
        self.__gender = info.__gender
        self.__avatar_path = info.__avatar_path
        self.__motto = info.__motto
        self.__address = info.__address
        self.__joined_time = info.__joined_time
        self.__grade = info.__grade
        self.__email = info.__email
        return True

    # ---------------------->插入用户信息的方法
    def insert(self):
        db.session.add(self)
        db.session.commit()
        return True

    # ---------------------->更改用户信息的方法
    '''update_dict 为修改后的所有信息形成的字典（包含所有可以后期改动的数据信息，无论是否有改动，均重新赋值）
    update_dict{'user': '2367821367'
                'new_gender': '你继续猜',
                'new_avatar': 'hiohoh',
                'new_motto': '我没什么好说的，怎么还没完成',
                'new_address': '江西上饶'}'''

    def update_user(self, update_dict):
        it = self.query.filter_by(__id=update_dict['user']).first()
        it.__gender = update_dict['new_gender']
        it.__avatar_path = update_dict['new_avatar']
        it.__motto = update_dict['new_motto']
        it.__address = update_dict['new_address']
        db.session.add(it)
        db.session.commit()

    # --------------------------->用户的操作部分

    # -------------------->用户宠物部分的操作
    # -------->新建宠物

    def create_pet(self, pet_dict):
        pet = Pet()
        pet_dict = pet.check_data(self.__id, pet_dict)
        if pet.create_pet(pet_dict) \
            and pet.insert():
            return True
        else:
            return False

    def get_user_pets(self):
        pet = Pet()
        pet_list = pet.user_all_pets(self.__id)
        return pet_list

    # -------------------->用户的卡片部分的操作
    # -------->获取时间轴
    def get_timeline(self, pet_id):
        #需要判断用户是否可以查看这只宠物的时间轴
        pet = Pet(pet_id = pet_id)
        if pet.get_whether_share() or \
            pet.get_user_id == self.__id:
            card = Card()
            timeline = card.timeline(pet)
            return timeline
        else:
            return False

    # 朋友圈方法，last_card_id是上次加载的最后一张卡片id
    # 朋友圈往下刷时，查找之前的朋友圈内容
    # 提供最下一条朋友圈的id，先查找出所有的关注人发的卡片，按时间排序，找到之前的动态
    def get_circle_of_friends(self, late_card_id):
        if late_card_id is None:
            #如果是第一次获取朋友圈，参数还未确认
            pass
        else:
            m = self.get_follow()
            _all = []
            show = []
            card = Card()
            for people in m:
                _all.append(card.get_one_all_share(people.__id))
            for i in len(_all):
                while _all[i]['id'] ==late_card_id:
                    for m in range(i,len(_all)+1):
                        show.append(_all[m])
            return show

    # -------->发布动态

    def create_card(self, card_dict):
        card = Card()
        card_dict = card.check_data(self.__id, card_dict)
        if card.create_card(card_dict) \
            and card.insert():
            return True
        else:
            return False

    def get_card_detail(self, card_id):
        card = Card(card_id)

        if card.get_card_id() is self.__id:
            return card.get_detail(card_id)
        elif card.get_whether_share():
            pet = Pet(pet_id = card.get_pet_id())
            if pet.get_whether_share:
                return card.get_detail(card_id)

        return False

    def get_hot_card(self):
        card = Card()
        hot = card.get_hot()
        return hot
        
    # -------------------->用户的评论部分的操作
    # --------->发布评论

    def create_comment(self, comment_dict):
        comment = Comment()
        comment_dict = comment.check_comment(self.__id, comment_dict)
        if comment.comment_on_card(comment_dict) \
            and comment.insert():
            return True
        else:
            return False

    # -------------------->用户的点赞部分的操作
    # --------->点赞和取消点赞

    def user_praise(self, be_praise_card_id, praise_operation):
        praise = Praise()
        if praise_operation == '1':
            return praise.create_praise(self.__id, be_praise_card_id)
        elif praise_operation == '0':
            return praise.del_praise(self.__id, be_praise_card_id)
        else:
            return False
    
    # --------------------->用户的关注部分的操作
    # --------->关注和取消关注

    def user_follow(self, be_concerned_id, follow_operation):
        follow = Follow()
        if follow_operation == '1':
            return follow.create_follow(self.__id, be_concerned_id)
        elif follow_operation == '0':
            return follow.del_follow(self.__id, be_concerned_id)
        else:
            return False

    # --------->获取用户关注用户
    def get_follow(self):
        follow = Follow()
        follow_dict = follow.find_followed_people(self.__id)
        return follow_dict

    # --------------------------->用户操作部分结束

    # --------------------------->用户属性部分
    # ---------->获取自己的信息
    def get_information(self):
        information = {
                    'id':self.__id,
                    'nickname': self.__user_nickname,
                    'gender': self.__gender,
                    'avator': self.__avatar_path,
                    'motto': self._motto,
                    'address': self._address,
                    'grade': self.__grade
                    }
        
        return information
    
    #获取他人的信息，user_id是查找的用户id
    def get_other_information(self,user_id):
        pass

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

    # --------------------------->用户属性部分结束
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