import uuid
import random
import time
from project import db
from .Tag import Tag
from .Tag_with_card import Tag_with_Card
from .PetLogDataError import PetLog_DataError

class Card(db.Model):
    """card model"""
    __tablename__ = "Cards"
    id = db.Column(db.String(16), primary_key=True, nullable=False)
    user_id = db.Column(db.String(16), nullable=False)
    pet_id = db.Column(db.String(16), nullable=False)
    pet_status = db.Column(db.String(20),nullable=True)
    content = db.Column(db.Text, nullable=True)
    images = db.Column(db.String(128), nullable=True)
    time = db.Column(db.Float, nullable=False)
    whether_share = db.Column(db.Integer,nullable = False)
    
    def __init__(self,card_id = None):
        if card_id:
            info = self.query.filter_by(id=card_id).all()
            self.id = info.id
            self.user_id = info.user_id
            self.pet_id = info.pet_id
            self.content = info.content
            self.images = info.images
            self.time = info.time
            self.whether_share = info.whether_share
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
        self.id = str(uuid.uuid1()).split("-")[0]
        self.user_id = create_dict['user_id']
        self.pet_id = create_dict['for']
        self.time = time.time()
        
        # 以下部分为发布卡片不一样要携带的信息
        self.set_content(create_dict['content'])
        self.set_images(create_dict['images'])

        self.whether_share = 1
        return True

    def insert(self):
        # 内容记录进数据库
        db.session.add(self)
        db.session.commit()
        return True

    def timeline(pet_id):
        items = []
        info = Card.query.filter(Card.pet_id == pet_id).\
                    order_by(Card.tag_id.asc()).all()
        if info is None:
            return []
        
        day = info[0].get_tm_yday()
        year = info[0].get_tm_year()

        one_day_items = []
        one_day = {
            "date":info[0].get_card_date(),
            "items":one_day_items,
            "is_year":False
        }
        one_year = {
            "date":"",
            "items":[],
            "is_year":True,
            "year":year
        }
        for i in info:
            one_card = {
                "content" : i.get_content(),
                "images" : i.get_images(),
                "status" : i.get_status(),
                "id" : i.get_id()
            }

            if (i.get_tm_yday() != day) or \
                (i.get_tm_year() != year):
                one_day['items'] = one_day_items
                items.append(one_day)
                one_day['items'] = [one_card]
                one_day["date"] = i.get_card_date(),
                day = i.get_tm_yday()
                if i.get_tm_year() != year:
                    items.append(one_year)
                    year = i.get_tm_year()
                    one_year['year'] = year
            else:
                one_day_items.append(one_card)

        return items

    def hot(cards_id):
        if cards_id:
            cards = Card.query.filter(Card.id.in_(cards_id)).all()
        else:
            cards = Card.query.all()
            
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
            data_dict['tags']
            data_dict['images']
            data_dict['status']
            # 内容和图片不能同时没有
            if not (data_dict['content'] or
                    data_dict['images']) or \
                not data_dict['for']:
                raise PetLog_DataError("Error : One post card lack something")
            else:
                data_dict['user_id'] = user_id
        except KeyError as error:
            print("KeyError : Don't has " + error)
            raise error
        except PetLog_DataError as error:
            print(error.message)
            raise error
        else:
            return data_dict

    #现在先随机从允许查看的卡片中抽取10条卡片，返回这个数组
    def get_hot_card(self):
        m = self.query.filter_by(card_type=1).all()
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
        qu = Card.query.filter(Card.user_id.in_(follows_ids))
        if tag_id :
            qu = qu.join(Tag_with_Card,Card.id==Tag_with_Card.id).\
                        filter(Tag_with_Card.tag_id == tag_id)
        if late_card_id:
            qu = qu.filter(Card.time < (Card.query.filter(
                            Card.id == late_card_id).first().get_time()))

        return qu.order_by(Card.time.asc()).limit(5).all()

    #返回一个人的所有相关卡片的信息
    def get_user_all_card(user_id,last_id):
        cards = Card.query.filter(Card.user_id == user_id).\
                        order_by(Card.time.asc())
        if last_id:
            last_time = Card.query.get(last_id).first().get_time()
            cards = cards.filter(Card.time <last_time)
        
        cards = cards.limit(5).all()
        all_cards =[]

        if cards is None:
            return all_cards
        else:
            for one_card in cards:
                post = {
                    "time": one_card.get_card_date(),
                    "content": one_card.get_content(),
                    "status": one_card.get_pet_status(),
                    "images": one_card.get_images()
                }

        return all_cards

    #返回一个宠物的所有相关卡片的信息
    def get_pet_all(self,pet_id): 
        pet_all_card = self.query.filter_by(pet_id=pet_id).all()
        return pet_all_card

    #返回一个用户的所有可分享的卡片：
    def get_one_all_share(self,user_id):
        share_all = self.query.filter_by(user_id=user_id,card_type=1).all()
        return share_all

    #返回一个宠物的所有可分享的卡片：
    def get_pet_all_share(self,pet_id):
        share_pet_all = self.query.filter_by(pet_id=pet_id,card_type=1).all()
        return share_pet_all
    
    #根据用户id判断是否可以获取卡片细节，如果是访客，user_id为guest
    def get_detail(self, card_id):
        information ={
                "id" : self.id,
                "user_id" : self.user_id,
                "pet_id" : self.pet_id,
                "card_content" : self.content,
                "card_image_path" : self.image_path,
                "card_time" : self.time,
                "card_type" : self.type,
                "whether_share" : self.whether_share
        }
        return information

    def get_id(self):
        return self.id

    def get_whether_share(self):
        if self.whether_share is 1:
            return True
        else:
            return False

    def get_time(self):
        return self.time

    def get_tm_yday(self):
        return time.localtime(self.get_time()).tm_yday

    def get_tm_year(self):
        return time.localtime(self.get_time()).tm_year

    def get_age(self):
        return time.localtime(time.time()).tm_year - \
                time.localtime(self.get_time()).tm_year
    
    def get_card_date(self):
        return time.strftime("%m-%d",time.localtime(
                                    self.get_time()))
                                    
    def get_user_id(self):
        return self.user_id
    
    def get_status(self):
        return self.pet_status

    def set_images(self,images):
        f_images = str()
        if images:
            for t in images:
                f_images = f_images + ' ' + t
                self.images = f_images
        else:
            self.images = None

    def set_content(self,content):
        if content:
            self.content =content
        else:
            self.content = None

