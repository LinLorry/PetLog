import uuid
from project import db
from .PetLogDataError import PetLog_DataError

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
        self.__pet_id = str(uuid.uuid1()).split("-")[0]
        self.__category = create_dict['category']
        self.__pet_name = create_dict['pet_name']
        self.__user_id = create_dict['user_id']
        self .__gender = create_dict['gender']
        self.__time = create_dict['time']
        return True

    def insert(self):
        # 内容记录进数据库
        db.session.add(self)
        db.session.commit()
        # session.close()
        return True

    def user_all_pet(self, user_id):
        # 时间轴界面下获取某用户所有宠物的id
        pets = self.query.filter_by(__user_id=user_id).all()
        all_pet = []
        for pet in pets:
            all_pet.append({'id': pet.__pet_id, 'name': pet.__pet_name})
        return all_pet
        # 返回某用户所有的宠物id（以列表套字典的格式返回）例：[{'id':'08980','name':'奥利奥'},{'id':'87389','name':'趣多多'}]
        # 时间轴界面会显示的有关宠物方面的信息（待补充）
    
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