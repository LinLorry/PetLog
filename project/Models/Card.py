import uuid
import random
import time
from project import db
from .Tag import Tag
from .Tag_with_card import Tag_with_Card
from .PetLogDataError import PetLog_DataError

class Card(db.Model):
    """card model"""
    __tablename__ = "cards"
    __id = db.Column(db.String(16), primary_key=True, nullable=False)
    __user_id = db.Column(db.String(16), nullable=False)
    __pet_id = db.Column(db.String(16), nullable=False)
    __card_content = db.Column(db.Text, nullable=True)
    __card_image_path = db.Column(db.String(128), nullable=True)
    __card_time = db.Column(db.DateTime, nullable=False)
    __card_type = db.Column(db.String(1),nullable=False)
    __tag_id = db.Column(db.String(256),nullable=True)
    __whether_share = db.Column(db.Integer,nullable = False)
    
    def __init__(self,card_id = None):
        if card_id:
            info = self.query.filter_by(_Card__id=card_id).all()
            self.__id = info.__id
            self.__user_id = info.__user_id
            self.__pet_id = info.__pet_id
            self.__card_content = info.__card_content
            self.__card_image_path = info.__card_image_path
            self.__card_time = info.__card_time
            self.__whether_share = info.__whether_share
        else:
            pass
    #------>发布动态

    def create_card(self, create_dict):
        # 创造卡片对象
        '''create_dict必须带的信息为：发布者的id,发布的内容（内容不得为空），相关的宠物的id,图片可以为空，标签不得为空。
        例如（仅是必须包括的信息的示例）：（标签不得为空，便于为卡片分类）
        {
            'content':'iihoi'，
            'petname':'奥利奥'，
            'pet_id':'989078989'，
            'user_id':'26372832673678',
            'tags':{"1","2"}
        }
        '''
        self.__id = str(uuid.uuid1()).split("-")[0]
        self.__user_id = create_dict['user_id']
        self.__content = create_dict['content']
        self.__pet_id = create_dict['pet_id']
        self.__card_type = create_dict['card_type']
        
        # 以下部分为发布卡片不一样要携带的信息
        self.set_images(create_dict['images'])
        self.set_tags(create_dict['tags'])
        self.__whether_share = 1
        return True

    def insert(self):
        # 内容记录进数据库
        db.session.add(self)
        db.session.commit()
        return True

    def timeline(self, pet):
        info = self.query.filter_by(__pet_id=pet.get_pet_id()).all()
        cards = {
            "name" : pet.get_name(),
            "age" : pet.get_age(),
            "avatar" : pet.get_avatar(),
            "mooto" : pet.get_motto(),
            "items" : []
        }
        if info is None:
            return cards
        items = []
        info = sorted(info,key = lambda s: s.get_time(),
                    reverse=True)
        
        one_card = {
            "content" : info[0].get_content(),
            "images" : info[0].get_images(),
            "status" : info[0].get_status(),
            "id" : info[0].get_id()
        }
        one_day = [one_card]
        one_item = {
            "date" : info[0].get_card_date(),
            "items" : [],
            "is_year" : False
        }

        day = info[0].get_tm_yday()
        year = info[0].get_tm_year()

        for i in info:
            if (i.get_tm_yday() != day) or \
                (i.get_tm_year() != year):
                one_item["items"] = one_day
                items.append(one_item)
                
                one_day = []
                one_item["date"] = i.get_card_date(),
                day = i.get_tm_yday()
                if i.get_tm_year() != year:
                    x = {
                        "date":"",
                        "items":[],
                        "is_year":True,
                        "year":year
                    }
                    items.append(x)
                    year = i.get_tm_year()
            
            one_card = {
                "content" : i.get_content(),
                "images" : i.get_images(),
                "status" : i.get_status(),
                "id" : i.get_id()
            }
            one_day.append(one_card)
        
        one_item["items"] = one_day
        items.append(one_item)

        cards['items'] = items
        return cards

    def hot(self,cards_id):
        cards = []
        for id in cards_id:
            cards.append(Card.query.filter(Card.__id == id).first())
        try:
            cards = random.sample(cards, 5)
            return cards
        except ValueError:
            try:
                cards = random.sample(cards, len(cards))
                return cards
            except:
                raise PetLog_DataError("can't get random cards")

    # 给卡片、状态、tags、share（Bool）
    def check_data(self, user_id, data_dict):
        try:
            # 内容和图片不能同时没有
            if not (data_dict['content'] or
                    data_dict['images']) or \
                    not data_dict['time']:
                raise PetLog_DataError("Error : One post card lack something")
            else:
                data_dict['time'] = int(data_dict['time']) * (10 ** -3)

            data_dict['user_id'] = user_id
        except KeyError as error:
            print("KeyError : Don't has " + error)
            raise KeyError
        except PetLog_DataError as error:
            print(error.message)
            raise PetLog_DataError
        else:
            return data_dict

    #现在先随机从允许查看的卡片中抽取10条卡片，返回这个数组
    def get_hot_card(self):
        m = self.query.filter_by(_Card__card_type=1).all()
        show = []
        n = []
        i = []
        if len(m)<10:
            return m
        else:
            while len(i) < 11 :
                n.append(m[random.randint(1,len(m))])
                i=list(set(n))
        for one in i:
            show.append(m[one])
        return show

    def get_followings_cards(follows_ids,tag_id,late_card_id):
        qu = Card.query.filter(Card.__user_id.in_(follows_ids))
        if tag_id :
            qu = qu.join(Tag_with_Card,Card.__id==Tag_with_Card.__card_id).\
                        filter(Tag_with_Card.__tag_id == tag_id)
        if late_card_id:
            qu = qu.filter(Card.__card_time < (Card.query.filter(
                            Card.__id == late_card_id).first().get_time()))

        return qu.order_by(Card.__card_time.asc()).limit(5).all()

    #返回一个人的所有相关卡片的信息
    def get_one_all(self,user_id):
        _all = self.query.filter_by(_Card__card_id=user_id).all()
        return _all

    #返回一个宠物的所有相关卡片的信息
    def get_pet_all(self,pet_id): 
        pet_all_card = self.query.filter_by(_Card__pet_id=pet_id).all()
        return pet_all_card

    #返回一个用户的所有可分享的卡片：
    def get_one_all_share(self,user_id):
        share_all = self.query.filter_by(_Card__user_id=user_id,_Card__card_type=1).all()
        return share_all

    #返回一个宠物的所有可分享的卡片：
    def get_pet_all_share(self,pet_id):
        share_pet_all = self.query.filter_by(_Card__pet_id=pet_id,_Card__card_type=1).all()
        return share_pet_all
    
    #根据用户id判断是否可以获取卡片细节，如果是访客，user_id为guest
    def get_detail(self, card_id):
        information ={
                "id" : self.__id,
                "user_id" : self.__user_id,
                "pet_id" : self.__pet_id,
                "card_content" : self.__card_content,
                "card_image_path" : self.__card_image_path,
                "card_time" : self.__card_time,
                "card_type" : self.__card_type,
                "whether_share" : self.__whether_share
        }
        return information

    def get_whether_share(self):
        if self.__whether_share is 1:
            return True
        else:
            return False

    def get_time(self):
        return self.__time

    def get_tm_yday(self):
        return time.localtime(self.get_time()).tm_yday

    def get_tm_year(self):
        return time.localtime(self.get_time()).tm_year
    
    def get_card_date(self):
        return time.strftime("%m-%d",time.localtime(
                                    self.get_time()))
                                    
    def get_user_id(self):
        return self.__user_id

    def set_images(self,images):
        f_images = str()
        for t in images:
            f_images = f_images + ' ' + t

        self.__images = f_images

    def set_tags(self,tags):
        tag_id = str()
        for t in tags:
            tag = Tag.filter_by(_Tags__name=t).all()
            if tag is None:
                raise PetLog_DataError("some tag don't in table!")
            tag_id = tag_id + ' ' + tag.get_id()

        self.__tag_id = tag_id
        return tag_id
