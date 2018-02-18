import uuid
from project import db

#----->关注功能

class Follow(db.Model):
    __tablename__ = "follow"
    __id = db.Column(db.String(16), primary_key=True, nullable=False)
    __user_id = db.Column(db.String(16), nullable=False)
    __be_concerned_id = db.Column(db.String(16), nullable=False)

    # 希望这两个方法成功后返回True,失败返回False
    # 不需要insert方法和update方法了，集成在这两个方法中

    def create_follow(self, user_id, be_concerned_id):
        try:
            __id = str(uuid.uuid1()).split("-")[0]
            self.__user_id = user_id
            self.__be_concerned_id = be_concerned_id
            db.session.add(self)
            db.session.commit()
        except:
            return False
        else:
            return True

    def del_follow(self, user_id, be_concerned_id):
        try:
            i = self.query.filter_by(
                __user_id=user_id, __be_concerned_id=be_concerned_id).first()
            db.session.delete(i)
            db.session.commit()
        except:
            return False
        else:
            return True

    def find_follow_number(self, user_id):  # 查找该用户关注的用户的数量为
        _all = self.query.filter_by(__user_id=user_id).all()
        f_number = len(_all)
        return f_number

    def find_followed_number(self, user_id):  # 查找有多少人关注该用户
        _all = self.query.filter_by(__be_concerned_id=user_id)
        fd_number = len(_all)
        return fd_number

    def show_follow_people(self, user_id):  # 显示出该用户关注的用户的初略信息
        from .User import User
        _all = self.query.filter_by(__user_id=user_id).all()
        f_people = []
        for a in _all:
            people = User.query.filter_by(__user_id=a.__user_id).first()
            f_people.append({'nickname': people.__user_nickname,
                             'grade': people.__grade,
                             'avatar': people.__avatar_path})
        # 返回的信息为：[{},{},{}]这样的形式，每个字典里为一个用户的初略信息。（返回初略的信息的内容待定）
        # 下面的方法返回的信息的格式同理。
        return f_people

    def find_followed_people(self, user_id):  # 显示出该用户被哪些人关注的初略信息
        from .User import User
        _all = self.query.filter_by(__be_concerned_id=user_id).all()
        fd_people = []
        for b in _all:
            people = User.query.filter_by(__user_id=b.__be_concerned_id).first
            fd_people.append({'nickname': people.__user_nickname,
                              'grade': people.__grade,
                              'avatar': people.__avatar_path})
        return fd_people