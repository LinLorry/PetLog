import uuid
from project import db


class Praise(db.Model):
    __tablename__ = "Praise"
    id = db.Column(db.String(16), primary_key=True)
    card_id = db.Column(db.String(16), nullable=False)
    user_id = db.Column(db.String(16), nullable=False)

    def create_praise(self, user_id, card_id):
        if not Praise.query.filter(Praise.card_id == card_id,
                                   Praise.user_id == user_id).first():
            self.id = str(uuid.uuid1()).split("-")[0]
            self.card_id = card_id
            self.user_id = user_id
            db.session.add(self)
            db.session.commit()
            return True
        else:
            return False

    def del_praise(self, user_id, card_id):
        try:
            i = self.query.filter_by(card_id=card_id, user_id=user_id).first()
            db.session.delete(i)
            db.session.commit()
        except:
            return False
        else:
            return True

    def find_praise_number(card_id):  # 查找某卡片的获赞的数量
        _all = Praise.query.filter(Praise.card_id == card_id).all()
        p_number = len(_all)
        return p_number

    def check_praise(user_id, card_id):
        if Praise.query.filter(Praise.user_id == user_id,
                               Praise.card_id == card_id).first():
            return True
        else:
            return False
