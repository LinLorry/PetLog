import uuid
import time
from project import db
from .PetLogDataError import PetLog_DataError


class Pet(db.Model):  # 待补充，宠物头像，以及宠物的介绍
    __tablename__ = "Pets"
    id = db.Column(db.String(16), nullable=False, primary_key=True)
    category = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.String(16), nullable=False)
    birth_day = db.Column(db.Float, nullable=False)
    gender = db.Column(db.String(8), nullable=False)
    avatar_path = db.Column(db.String(128), nullable=False)

    whether_share = db.Column(db.Boolean, nullable=False)
    motto = db.Column(db.Text, nullable=True)
    meet_day = db.Column(db.Float, nullable=False)

    # 宠物的构造函数，用于查找一个宠物
    def __init__(self, pet_id=None):
        if pet_id:
            info = self.query.filter_by(id=pet_id).first()

            if info is None:
                raise PetLog_DataError("Don't have this id : " + pet_id)

            self.id = info.id
            self.category = info.category
            self.name = info.name
            self.user_id = info.user_id
            self.birth_day = info.birth_day
            self.gender = info.gender
            self.whether_share = info.whether_share
            self.avatar_path = info.avatar_path
            self.motto = info.motto
            self.meet_day = info.meet_day
        else:
            pass

    def create_pet(self, create_dict):
        # 宠物唯一id的生成
        self.id = str(uuid.uuid1()).split("-")[0]
        self.category = create_dict['variety']
        self.name = create_dict['name']
        self.user_id = create_dict['user_id']
        self.gender = create_dict['gender']
        self.set_birth_day(create_dict['birth_day'])
        self.set_meet_day(create_dict['meet_day'])
        self.whether_share = True
        self.avatar_path = create_dict['avatar']
        self.motto = create_dict['motto']
        return True

    def insert(self):
        # 内容记录进数据库
        db.session.add(self)
        db.session.commit()
        return True

    def update(self, update_dict):
        that = self.query.filter_by(id=update_dict['id']).first()
        that.name = update_dict['name']
        that.motto = update_dict['motto']
        that.avatar = update_dict['avatar']
        that.gender = update_dict['gender']
        that.set_birth_day(update_dict['birth_day'])
        that.set_meet_day(update_dict['meet_day'])
        that.category = update_dict['variety']
        db.session.add(that)
        db.session.commit()

        return True

    def user_all_pets(user_id):
        # 时间轴界面下获取某用户所有宠物的id
        pets = Pet.query.filter_by(user_id=user_id).all()
        all_pets = []
        for pet in pets:
            all_pets.append({
                'id': pet.get_id(),
                'name': pet.get_name(),
                "avatar": pet.get_avatar()
            })
        return all_pets

    def check_data(self, user_id, data_dict):
        try:
            if Pet.query.filter(Pet.user_id == user_id,
                                Pet.name == data_dict['name']).first():
                raise PetLog_DataError(
                    "This usre : %s,his pet : %s is exist!" %
                    (user_id, data_dict['name']))
            elif not data_dict['motto'] or \
                    not data_dict['variety'] or \
                    not data_dict['gender'] or \
                    not data_dict['meet_day'] or \
                    not data_dict['birth_day'] or \
                    not data_dict['avatar'] or\
                    not data_dict['gender']:
                raise PetLog_DataError('One create_pet lack something')
            else:
                data_dict['user_id'] = user_id
        except KeyError as error:
            print("Error : dict lack some key!")
            raise error
        except PetLog_DataError as error:
            raise error
        else:
            return data_dict

    def check_update_data(self, data_dict):
        if not data_dict['name'] or \
            not data_dict['id']  or \
            not data_dict['motto'] or \
            not data_dict['avatar'] or \
            not data_dict['gender'] or \
            not data_dict['birth_day'] or \
            not data_dict['meet_day'] or \
            not data_dict['variety'] :
            return False
        else:
            return True

    def get_detail(pet_id, user_id):
        info = Pet.query.get(pet_id)
        if info.get_user_id() == user_id:
            return {
                "status": 1,
                "message": "已经找到您的宠物",
                "name": info.get_name(),
                "motto": info.get_motto(),
                "avatar": info.get_avatar(),
                "gender": info.get_gender(),
                "birth_day": info.get_birth(),
                "meet_day": info.get_meet(),
                "variety": info.get_category()
            }
        else:
            return {"status": 0, "message": "不好意思，这不是您的宠物"}

    def get_whether_share(self):
        return self.get_whether_share

    def get_user_id(self):
        return self.user_id

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_avatar(self):
        return self.avatar_path

    def get_motto(self):
        if self.motto:
            return self.motto
        else:
            return None

    def get_birth_day(self):
        return self.birth_day

    def get_meet_day(self):
        return self.meet_day

    def get_birth(self):
        return time.strftime("%Y-%m-%d", time.localtime(self.get_birth_day()))

    def get_meet(self):
        return time.strftime("%Y-%m-%d", time.localtime(self.get_meet_day()))

    def get_age(self):
        return time.localtime(time.time()).tm_year - \
                time.localtime(self.get_birth_day()).tm_year

    def get_gender(self):
        return self.gender

    def get_category(self):
        return self.category

    def set_birth_day(self, birth_day):
        self.birth_day = time.mktime(time.strptime(birth_day, "%Y-%m-%d"))

    def set_meet_day(self, meet_day):
        self.meet_day = time.mktime(time.strptime(meet_day, "%Y-%m-%d"))
