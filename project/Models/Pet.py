import uuid
from project import db
from .PetLogDataError import PetLog_DataError

class Pet(db.Model):  # 待补充，宠物头像，以及宠物的介绍
    __tablename__ = "pets"
    __pet_id = db.Column(db.String(16), nullable=False, primary_key=True)
    __category = db.Column(db.String(32), nullable=False)

    __pet_name = db.Column(db.String(20), nullable=False)
    __user_id = db.Column(db.String(16), nullable=False)
    __birth_day = db.Column(db.DateTime, nullable=False)
    __gender = db.Column(db.String(8), nullable=False)
    __pet_avatar_path = db.Column(db.String(128),nullable = False)

    __whether_share = db.Column(db.Integer,nullable = False)
    __motto = db.Column(db.Text,nullable = True)
    __meet_day = db.Column(db.DateTime,nullable = False)

    # 宠物的构造函数，用于查找一个宠物
    def __init__(self, pet_id = None):
        if pet_id:
            info = self.query.filter_by(_Pet__id=pet_id).first()

            if info is None:
                raise PetLog_DataError("Don't have this id : " + pet_id)

            self.__pet_id = info.__pet_id
            self.__category = info.__category
            self.__detailed_category = info.__detailed_category
            self.__pet_name =info.__pet_name
            self.__gender = info.__gender
            self.__user_id = info.__user_id
            self.__gender = info.__gender
            self.__whether_share = info.__whether_share
            self.__pet_avatar_path = info.__pet_avatar_path
        else:
            pass

    def create_pet(self, create_dict):
        # 宠物唯一id的生成
        self.__pet_id = str(uuid.uuid1()).split("-")[0]
        self.__category = create_dict['variety']
        self.__pet_name = create_dict['name']
        self.__user_id = create_dict['user_id']
        self.__gender = create_dict['gender']
        self.__birth_day = create_dict['birth_day']
        self.__whether_share = 1
        self.__meet_day = create_dict['meet_day']
        self.__pet_avatar_path = create_dict['avatar']
        self.__motto = create_dict['motto']
        return True

    def insert(self):
        # 内容记录进数据库
        db.session.add(self)
        db.session.commit()
        return True

    def update(self,update_dict):
        that = self.query.filter_by(_Pet__pet_id=update_dict['id']).first()
        that.__pet_name = update_dict['name']
        that.__motto = update_dict['motto']
        that.__avatar = update_dict['avatar']
        that.__gender = update_dict['gender']
        that.__birth_day = update_dict['birth_day']
        that.__meet_day = update_dict['meet_day']
        that.__category = update_dict['variety']
        db.session.add(that)
        db.session.commit()
        
        return True

    def user_all_pet(self, user_id):
        # 时间轴界面下获取某用户所有宠物的id
        pets = self.query.filter_by(__user_id=user_id).all()
        all_pets = []
        for pet in pets:
            all_pets.append({'id': pet.get_id(), 
                        'name': pet.get_name(),
                        "avatar":pet.get_avatar()})
        return all_pets

    def check_data(self, user_id, data_dict):
        try:
            data_dict['detailed_category']
            data_dict['gender']
            data_dict['pet_avatar_path']
            if not data_dict['pet_name'] or \
                    not data_dict['category'] or \
                    not data_dict['gender'] or \
                    not data_dict['time']:
                raise PetLog_DataError(
                    'One create_pet lack something')
            else:
                data_dict['user_id'] = user_id
        except KeyError as error:
            print ("Error : dict lack some key!")
            raise error
        except PetLog_DataError as error:
            print ("Error : One create_pet lack something can't be None!")
            raise error
        else:
            return data_dict

    def find_by_id(self, pet_id):  # 传入某一用户的id 返回的是某人的详细信息
        info = self.query.filter_by(_Pet__id=pet_id).first()

        if info is None:
            raise PetLog_DataError("Don't have this id : " + pet_id)

        self.__pet_id = info.__pet_id
        self.__category = info.__category
        self.__detailed_category = info.__detailed_category
        self.__pet_name =info.__pet_name
        self.__gender = info.__gender
        self.__user_id = info.__user_id
        self.__gender = info.__gender
        self.__whether_share = info.__whether_share
        self.__pet_avatar_path = info.__pet_avatar_path

        #......不止这些还有其他的内容
        return True
    
    def get_detail(pet_id):
        info = Pet.get(pet_id)
        detail ={
            "name": info.get_id(),
            "motto": info.get_motto(),
            "avatar": info.get_avatar(),
            "gender": info.get_gender(),
            "birth_day": info.get_birth(),
            "meet_day": info.get_meet(),
            "variety": info.get_category()
        }
        return detail


    def get_whether_share(self):
        if self.get_whether_share is 1:
            return True
        else:
            return False
            
    def get_user_id(self):
        return self.__user_id

    def get_id(self):
        return self.__pet_id

    def get_name(self):
        return self.__pet_name

    def get_avatar(self):
        return self.__pet_avatar_path