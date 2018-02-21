import uuid
from project import db
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
        self.__id = str(uuid.uuid1()).split("-")[0]
        self.__user_id = create_dict['user_id']
        self.__content = create_dict['content']
        self.__pet_id = create_dict['pet_id']
        self.__card_type = create_dict['card_type']
        
        # 以下部分为发布卡片不一样要携带的信息
        self.__images = create_dict['images']
        self.__tags = create_dict['tags']
        pass

    def set_card_image(self, card_image):
        pass

    def insert(self):
        # 内容记录进数据库
        db.session.add(self)
        db.session.commit()
        return True

    def time_card(self, user_id):
        from .User import User
        user = User(content=user_id,option='id')
        that = user.user_all_pet(user_id)
        num = len(that)
        for i in range(len(that)):
            pet = that[i]['id']
            cards = self.query.filter_by(__pet_id=pet).all()
            # 找到所有该宠物的卡片
            # 之后按照时间排序，分组，返回以一个月为一组的数据。

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
    def get_one_all_share(self,pet_id):
        share_pet_all = self.query.filter_by(_Card__pet_id=pet_id,_Card__card_type=1).all()
        return share_pet_all
    
