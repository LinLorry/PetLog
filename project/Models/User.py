import uuid
import time
from threading import Thread
from flask import current_app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from project import db
from .Pet import Pet
from .Tag import Tag
from .Card import Card
from .Praise import Praise
from .Follow import Follow
from .Comment import Comment
from .Tag_with_card import Tag_with_Card
from .PetLogDataError import PetLog_DataError


class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.String(16), primary_key=True, nullable=False)
    email = db.Column(db.String(32), unique=True, nullable=False)
    nickname = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    avatar_path = db.Column(db.String(128), nullable=False)
    motto = db.Column(db.String(256), nullable=True)
    address = db.Column(db.String(30), nullable=False)
    birth = db.Column(db.Float, nullable=True)
    joined_time = db.Column(db.Float, nullable=False)
    grade = db.Column(db.Integer, nullable=False)

    # 构造函数
    #用来构造一个访客的用户对象
    def __init__(self, content=None, option="default"):
        if option == 'id' or \
            option == 'email':
            if option == 'id':
                info = User.query.filter(User.id == content).first()
            elif option == 'email':
                info = User.query.filter(User.email == content).first()
            self.id = info.get_id()
            self.nickname = info.nickname
            self.password_hash = info.password_hash
            self.address = info.address
            self.gender = info.gender
        elif option == 'default':
            pass
        elif option == 'guest':
            pass

    def verify_data(data_dict, verify_type):
        try:
            if verify_type == "register":
                # 用户必须有邮箱，昵称和密码
                if not data_dict['email'] or \
                    not data_dict['user_nickname'] or \
                    not data_dict['password'] or \
                    not data_dict['gender'] or \
                    not data_dict['avatar'] or \
                    not data_dict['gender'] :
                    raise PetLog_DataError("One register lack something")
            elif verify_type == "auth":
                # 验证登陆一定有邮箱和密码
                if not data_dict['email'] or \
                    not data_dict['password']:
                    raise PetLog_DataError("One login lack something")
            elif verify_type == "update":
                if not data_dict['name'] or \
                    not data_dict['gender'] or \
                    not data_dict['avatar'] or \
                    not data_dict['location']:
                    raise PetLog_DataError("One update lack something")
                data_dict['motto']
                data_dict['birth_day']

        except KeyError as error:
            print("KeyError : Don't has " + str(error))
            raise error

        except PetLog_DataError as error:
            print("Error : " + error.message)
            raise error

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
        self.id = str(uuid.uuid1()).split("-")[0]

        # 对于必须拥有的变量调用赋值即可
        self.email = create_dict['email']
        self.nickname = create_dict['user_nickname']
        self.password = create_dict['password']
        self.joined_time = time.time()

        self.grade = 1  # 直接赋值，初始用户等级均为1
        self.avatar_path = create_dict['avatar']

        # 对于不一定拥有的变量调用set设置器（由后端自动生成字段）
        # 有些设置器还未写,需要补充(若为空赋值为后面的结果)

        self.set_address(create_dict['address'])
        self.set_gender(create_dict['gender'])

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
        update_dict = User.verify_data(update_dict, "update")
        it = User.query.get(self.get_id())
        it.nickname = update_dict['name']
        it.gender = update_dict['gender']
        it.avatar_path = update_dict['avatar']
        it.motto = update_dict['motto']
        it.address = update_dict['location']
        it.set_birth(update_dict['birth_day'])
        db.session.add(it)
        db.session.commit()
        return True

    # --------------------------->用户的操作部分

    # -------------------->用户宠物部分的操作
    # -------->新建宠物

    def create_pet(self, pet_dict):
        pet = Pet()
        pet_dict = pet.check_data(self.get_id(), pet_dict)

        if pet.create_pet(pet_dict) \
            and pet.insert():
            return pet.get_id()
        else:
            return False

    def get_all_pets(self):
        pets = Pet.user_all_pets(self.get_id())
        pet_list = {"status": 1, "pets": pets}
        return pet_list

    def get_pet_detail(self, pet_id):
        return Pet.get_detail(pet_id, self.get_id())

    def update_pet(self, pet_dict):
        pet = Pet()
        if pet.check_update_data(pet_dict):
            pet.update(pet_dict)
            return True
        else:
            return False

    # -------------------->用户的卡片部分的操作

    # -------->发布动态

    def create_card(self, card_dict):
        card = Card()
        card_dict = card.check_data(self.get_id(), card_dict)
        if card.create_card(card_dict):
            t_w_c = Tag_with_Card()
            tags_id = []
            for tag_name in card_dict['tags']:
                tags_id.append(Tag.get_id(tag_name))
            if t_w_c.create_tag_with_card(card.get_id(),tags_id) \
                and card.insert():
                return True
        return False

    # -------->获取时间轴
    def get_timeline(self, pet_id):
        #需要判断用户是否可以查看这只宠物的时间轴
        pet = Pet.query.get(pet_id)
        if pet is None:
            raise ("Don't have this pet id!")

        timeline = {
            "name": pet.get_name(),
            "age": pet.get_age(),
            "avatar": pet.get_avatar(),
            "mooto": pet.get_motto(),
            "items": []
        }
        if pet.get_id() == self.get_id():
            timeline['status'] = 1
        elif pet.get_whether_share():
            timeline['status'] = 0
        else:
            return False

        timeline['items'] = Card.timeline(pet_id)

        return timeline

    # 朋友圈方法，last_card_id是上次加载的最后一张卡片id
    # 朋友圈往下刷时，查找之前的朋友圈内容
    # 提供最下一条朋友圈的id，先查找出所有的关注人发的卡片，按时间排序，找到之前的动态
    def get_circle_of_friends(self, tags_name, late_card_id):
        followings_id = Follow.get_followings_id(self.get_id())
        if tags_name:
            tags_id = []
            for tag_name in tags_name:
                tags_id.append(Tag.get_id(tag_name))
        else:
            tags_id = None

        cards = Card.get_followings_cards(followings_id, tags_id, late_card_id)
        if len(cards) < 5:
            infinited = True
        else:
            infinited = False

        friend = {"infinited": infinited, "cards": self.trans_card(cards)}

        return friend

    def get_hot_card(self, tags_name):
        if tags_name:
            cards_id = []
            for tag_name in tags_name:
                tag_id = Tag.get_id(tag_name)
                cards_id + Tag_with_Card.get_cid_with_tid(tag_id)

            if cards_id is []:
                return {"infinited": True, "cards": []}
        else:
            cards_id = None

        cards = Card.hot(cards_id)

        if len(cards) < 5:
            infinited = True
        else:
            infinited = False

        hot = {"infinited": infinited, "cards": self.trans_card(cards)}
        return hot

    def get_user_all_card(self, user_id, last_id):
        if not user_id:
            raise PetLog_DataError("One query user cards don't has user id.")

        cards = Card.get_user_all_card(user_id, last_id)
        for card in cards:
            card['liked'] = Praise.check_praise(self.get_id(), card['id'])
            card['comments'] = Comment.\
                    get_comments_with_card_number(
                        card['id'])
            for tag_id in Tag_with_Card.get_tid_with_cid(card['id']):
                card['post']['tags'].append(Tag.get_name(tag_id))
            card['post']['likes'] = Praise.find_praise_number(card['id'])

        return cards

    def trans_card(self, cards):
        all_card = []
        for card in cards:
            user = User.query.get(card.get_user_id())
            id = card.get_id()
            author = {
                "name": user.get_nickname(),
                "id": user.get_id(),
                "avatar": user.get_avatar(),
                "followed": Follow.check_follow(self.get_id(), user.get_id())
            }
            liked = Praise.check_praise(self.get_id(), card.get_id())
            post = {
                "time": card.get_card_date(),
                "content": card.get_content(),
                "status": card.get_pet_status(),
                "tags": [],
                "likes": Praise.find_praise_number(card.get_id()),
                "images": card.get_images()
            }

            for tag_id in Tag_with_Card.get_tid_with_cid(card.get_id()):
                post['tags'].append(Tag.get_name(tag_id))
            comments = Comment.get_comments_with_card_number(card.get_id())
            one_card = {
                "id": id,
                "author": author,
                "liked": liked,
                "post": post,
                "comments": comments
            }
            all_card.append(one_card)
        return all_card

    def get_card_detail(self, card_id):
        card = Card.query.get(card_id)
        if card.get_user_id() == self.get_id():
            author = self
            post = card.get_detail(card_id)
        elif card.get_whether_share():
            pet = Pet(pet_id=card.get_pet_id())
            if pet.get_whether_share:
                author = User.query.get(card.get_user_id())
                post = card.get_detail(card_id)
        else:
            return False

        post['like'] = Praise.find_praise_number(card.get_id())
        author_card = card.get_user_id()
        author_detail = {
            "name": author.get_nickname(),
            "id": author.get_id(),
            "avatar": author.get_avatar(),
            "followed": Follow.check_follow(self.get_id(), author.get_id())
        }

        comments = []
        for comment in Comment.get_comments(card_id):
            author_ = User.query.get(comment.get_user_id())
            author__detail = {
                "name": author_.get_nickname(),
                "id": author_.get_id(),
                "avatar": author_.get_avatar()
            }
            if comment.get_reply_id() == None:
                pd = True
                pp = "作者"
            else:
                pd = False
                pp = comment.get_reply_id()
            one_comment = {
                "id": comment.get_id(),
                "author": author__detail,
                "to_author": pd,
                "reply_to": pp,
                "time": comment.get_date(),
                "content": comment.get_content()
            }
            comments.append(one_comment)

        detail = {
            "id": self.get_id(),
            "author": author_detail,
            "liked": Praise.check_praise(self.get_id(), card_id),
            "post": post,
            "comments": comments
        }
        return detail

    # -------------------->用户的评论部分的操作
    # --------->发布评论

    def create_comment(self, comment_dict):
        comment = Comment()
        comment_dict['user_id'] = self.id
        comment_dict = comment.check_data(self.id, comment_dict)
        if comment.comment_on_card(comment_dict) \
            and comment.insert():
            return comment.get_tm_date()
        else:
            return False

    # -------------------->用户的点赞部分的操作
    # --------->点赞和取消点赞

    def user_praise(self, be_praise_card_id, praise_operation):
        praise = Praise()
        if praise_operation == 1:
            return praise.create_praise(self.id, be_praise_card_id)
        elif praise_operation == 0:
            return praise.del_praise(self.id, be_praise_card_id)
        else:

            return False

    # --------------------->用户的关注部分的操作
    # --------->关注和取消关注

    def user_follow(self, be_concerned_id, follow_operation):
        if be_concerned_id == self.get_id():
            return False
        follow = Follow()
        if follow_operation == '1':
            return follow.create_follow(self.id, be_concerned_id)
        elif follow_operation == '0':
            return follow.del_follow(self.id, be_concerned_id)
        else:
            return False

    def get_followers(self):
        followers_id = Follow.get_followers_id(self.get_id())
        followers = []

        for id in followers_id:
            user = User.query.get(id)
            follower = {
                "name": user.get_nickname(),
                "id": user.get_id(),
                "avatar": user.get_avatar(),
                "motto": user.get_motto(),
                "followed": Follow.check_follow(self.get_id(), user.get_id())
            }
            followers.append(follower)

        return followers

    # --------->获取用户关注用户
    def get_followings(self):
        follow = Follow()
        followings_id = Follow.get_followings_id(self.get_id())
        followings = []

        for u_id in followings_id:
            user = User.query.get(u_id)
            following = {
                "name": user.get_nickname(),
                "id": user.get_id(),
                "avatar": user.get_avatar(),
                "motto": user.get_motto(),
                "followed": Follow.check_follow(self.get_id(), user.get_id())
            }
            followings.append(following)

        return followings

    # --------------------------->用户操作部分结束

    # --------------------------->用户属性部分

    def get_profile_summary(self):
        user = {
            "name": self.get_nickname(),
            "avatar": self.get_avatar(),
            "followers": Follow.get_followers_number(self.get_id()),
            "followings": Follow.get_followings_number(self.get_id()),
            "motto": self.get_motto()
        }
        return user

    def get_profile(self):
        user = {
            "name": self.get_nickname(),
            "avatar": self.get_avatar(),
            "motto": self.get_motto(),
            "gender": self.get_gender(),
            "birth_day": self.get_birth_day(),
            "location": self.get_location()
        }
        return user

    #获取他人的信息，user_id是查找的用户id
    def get_other_profile(self, user_id):
        other = User.query.get(user_id)

        followed = Follow.check_follow(self.get_id(), other.get_id())
        user = {
            "name": other.get_nickname(),
            "avatar": other.get_avatar(),
            "motto": other.get_motto(),
            "followers": Follow.get_followers_number(other.get_id()),
            "following": Follow.get_followings_number(other.get_id())
        }
        pets = Pet.user_all_pets(other.get_id())

        return {"followed": followed, "user": user, "pets": pets}

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # 稍微修改了密码的hash算法
    # 密码hash用"密码+用户名+salt"的方法来算
    @password.setter
    def password(self, password):
        self.password_hash = pwd_context.encrypt(
            password + current_app.config['SALT'] + self.id)

    # 校验密码方法
    def verify_password(self, password):
        return pwd_context.verify(
            password + current_app.config['SALT'] + self.id,
            self.password_hash)

    # --------------------------->用户属性部分结束

    # 获取token的方法，默认时间是10分钟(10*60秒)
    # 密钥使用配置属性，配置属性来自系统变量在project.__init__.py里
    # 加上用户名好在检查token结束后，构造用户对象
    def generate_auth_token(self, expiration=7200):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id, 'email': self.email})

    # 计算用户当前等级的方法
    def grade_now(self, grade, user_id, comment_number, praise_number):

        # 具体计算待定
        return grade

    # ------------------------>查找用户的方法(通过昵称搜索用户)

    def find_all_user_number(self, nickname):  # 传入要找的用户的昵称
        peoples = self.query.filter_by(user_nickname=nickname).all()
        number = len(peoples)
        return number  # 返回的为同一昵称的用户的总数

    def find_all_user(self, nickname):  # 传入要找的用户的昵称
        peoples = self.query.filter_by(user_nickname=nickname).all()
        users = []
        for people in peoples:
            users.append({
                'nickname': people.nickname,
                'avatar': people.avatar_path,
                'joined_time': people.joined_time
            })
        return users  # 由于名称可重复，返回的为同一昵称的用户的id列表

    # --------->(查询自身信息,查询某人的详细信息）

    def find_by_email(self, user_email):
        info = self.query.filter_by(email=user_email).first()
        if info is None:
            raise PetLog_DataError("Don't have this email : " + user_email)

        self.id = info.id
        self.nickname = info.nickname
        self.password_hash = info.password_hash
        self.gender = info.gender
        self.avatar_path = info.avatar_path
        self.motto = info.motto
        self.address = info.address
        self.joined_time = info.joined_time
        self.grade = info.grade
        self.email = info.email
        return True

    # ---------------------------->get

    def get_nickname(self):
        return self.nickname

    def get_id(self):
        return self.id

    def get_motto(self):
        if self.motto:
            return self.motto
        else:
            return "空"

    def get_avatar(self):
        return self.avatar_path

    def get_gender(self):
        return self.gender

    def get_birth_day(self):
        return time.strftime("%Y-%m-%d", time.localtime(self.birth))

    def get_location(self):
        return self.address

    # ---------------------------->get结束

    # ---------------------------->设置器(set)

    def set_address(self, address):
        if not address == '':
            self.address = address
        return True

    def set_gender(self, gender):
        if not gender == '':
            self.gender = gender
        return True

    def set_motto(self, motto):
        if not motto == '':
            self.motto = motto
        return True

    def set_birth(self, birth_day):
        self.birth = time.mktime(time.strptime(birth_day, "%Y-%m-%d"))
        return True

    # ---------------------------->设置器(set)结束
