import uuid
import time
from project import db
from .PetLogDataError import PetLog_DataError

class Pet(db.Model):  # 待补充，宠物头像，以及宠物的介绍
    __tablename__ = "Pets"
    pet_id = db.Column(db.String(16), nullable=False, primary_key=True)
    category = db.Column(db.String(32), nullable=False)
    pet_name = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.String(16), nullable=False)
    birth_day = db.Column(db.Float, nullable=False)
    gender = db.Column(db.String(8), nullable=False)
    pet_avatar_path = db.Column(db.String(128),nullable = False)

    whether_share = db.Column(db.Integer,nullable = False)
    motto = db.Column(db.Text,nullable = True)
    meet_day = db.Column(db.Float,nullable = False)

    # 宠物的构造函数，用于查找一个宠物
    def __init__(self, pet_id = None):
        if pet_id:
            info = self.query.filter_by(id=pet_id).first()

            if info is None:
                raise PetLog_DataError("Don't have this id : " + pet_id)

            self.pet_id = info.pet_id
            self.category = info.category
            self.pet_name =info.pet_name
            self.user_id = info.user_id
            self.birth_day = info.birth_day
            self.gender = info.gender
            self.whether_share = info.whether_share
            self.pet_avatar_path = info.pet_avatar_path
            self.motto = info.motto
            self.meet_day = info.meet_day
        else:
            pass

    def create_pet(self, create_dict):
        # 宠物唯一id的生成
        self.pet_id = str(uuid.uuid1()).split("-")[0]
        self.category = create_dict['variety']
        self.pet_name = create_dict['name']
        self.user_id = create_dict['user_id']
        self.gender = create_dict['gender']
        self.set_birth_day(create_dict['birth_day'])
        self.set_meet_day(create_dict['meet_day'])
        self.whether_share = 1
        self.pet_avatar_path = create_dict['avatar']
        self.motto = create_dict['motto']
        return True

    def insert(self):
        # 内容记录进数据库
        db.session.add(self)
        db.session.commit()
        return True

    def update(self,update_dict):
        that = self.query.filter_by(pet_id=update_dict['id']).first()
        that.pet_name = update_dict['name']
        that.motto = update_dict['motto']
        that.avatar = update_dict['avatar']
        that.gender = update_dict['gender']
        that.set_birth_day(update_dict['birth_day'])
        that.set_meet_day(update_dict['meet_day'])
        that.category = update_dict['variety']
        db.session.add(that)
        db.session.commit()
        
        return True

    def user_all_pet(self, user_id):
        # 时间轴界面下获取某用户所有宠物的id
        pets = self.query.filter_by(user_id=user_id).all()
        all_pets = []
        for pet in pets:
            all_pets.append({'id': pet.get_id(), 
                        'name': pet.get_name(),
                        "avatar":pet.get_avatar()})
        return all_pets

    def check_data(self, user_id, data_dict):
        try:
            if Pet.query.filter(Pet.user_id == user_id,
                    Pet.pet_name == data_dict['name']):
                raise PetLog_DataError(
                    "This usre : %s,his pet : %s is exist!" % 
                    (user_id,data_dict['name']))
            elif not data_dict['motto'] or \
                    not data_dict['variety'] or \
                    not data_dict['gender'] or \
                    not data_dict['meet_day'] or \
                    not data_dict['birth_day'] or \
                    not data_dict['avatar'] or\
                    not data_dict['gender']:
                raise PetLog_DataError(
                    'One create_pet lack something')
            else:
                data_dict['user_id'] = user_id
        except KeyError as error:
            print ("Error : dict lack some key!")
            raise error
        except PetLog_DataError as error:
            raise error
        else:
            return data_dict
        
    def check_update_data(self,data_dict):
        if data_dict['name'] is  None:
            return "名字不得为空"
        else:
            return True

    def find_by_id(self, pet_id):  # 传入某一用户的id 返回的是某人的详细信息
        info = self.query.filter_by(id=pet_id).first()

        if info is None:
            raise PetLog_DataError("Don't have this id : " + pet_id)

        self.pet_id = info.pet_id
        self.category = info.category
        self.detailed_category = info.detailed_category
        self.pet_name =info.pet_name
        self.gender = info.gender
        self.user_id = info.user_id
        self.gender = info.gender
        self.whether_share = info.whether_share
        self.pet_avatar_path = info.pet_avatar_path

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
        return self.user_id

    def get_id(self):
        return self.pet_id

    def get_name(self):
        return self.pet_name

    def get_avatar(self):
        return self.pet_avatar_path

    def set_birth_day(self,birth_day):
        self.birth_day = time.mktime(time.strptime(birth_day,"%Y-%m-%d"))
    
    def set_meet_day(self,meet_day):
        self.meet_day = time.mktime(time.strptime(meet_day,"%Y-%m-%d"))
