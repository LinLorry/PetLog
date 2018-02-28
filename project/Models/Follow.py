import uuid
from project import db

#----->关注功能


class Follow(db.Model):
    __tablename__ = "Follow"
    id = db.Column(db.String(16), primary_key=True)
    user_id = db.Column(db.String(16), nullable=False)
    be_concerned_id = db.Column(db.String(16), nullable=False)

    def create_follow(self, user_id, be_concerned_id):
        if not Follow.query.filter(Follow.be_concerned_id == be_concerned_id,
                                   Follow.user_id == user_id).first():
            self.id = str(uuid.uuid1()).split("-")[0]
            self.user_id = user_id
            self.be_concerned_id = be_concerned_id
            db.session.add(self)
            db.session.commit()
            return True
        else:
            return False

    def del_follow(self, user_id, be_concerned_id):
        try:
            i = self.query.filter_by(
                user_id=user_id, be_concerned_id=be_concerned_id).first()
            db.session.delete(i)
            db.session.commit()
        except:
            return False
        else:
            return True

    def find_followed_people(self, user_id):  # 显示出该用户被哪些人关注的初略信息
        from .User import User
        _all = self.query.filter_by(be_concerned_id=user_id).all()
        fd_people = []
        for b in _all:
            people = User.query.filter_by(user_id=b.be_concerned_id).first
            fd_people.append({
                'nickname': people.user_nickname,
                'grade': people.grade,
                'avatar': people.avatar_path
            })
        return fd_people

    def get_following_id(self):
        return self.be_concerned_id

    def get_follower_id(self):
        return self.user_id

    def get_followers_id(user_id):
        followers_id = []
        for follower in Follow.query.filter(
                Follow.be_concerned_id == user_id).all():
            followers_id.append(follower.get_follower_id())
        return followers_id

    def get_followings_id(user_id):
        followings_id = []
        for following in Follow.query.filter(Follow.user_id == user_id).all():
            followings_id.append(following.get_following_id())
        return followings_id

    def get_followers_number(user_id):  # 查找有多少人关注该用户
        _all = Follow.query.filter(Follow.be_concerned_id == user_id).all()
        if _all is None:
            return 0
        fer_number = len(_all)
        return fer_number

    def get_followings_number(user_id):  # 查找该用户关注的用户的数量为
        _all = Follow.query.filter(Follow.user_id == user_id).all()
        if _all is None:
            return 0
        fing_number = len(_all)
        return fing_number

    def check_follow(follower_id, following_id):
        if Follow.query.filter(Follow.user_id == follower_id,
                               Follow.be_concerned_id == following_id).first():
            return True
        else:
            return False
