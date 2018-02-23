import uuid
import time
from project import db
from .PetLogDataError import PetLog_DataError

#----->评论方面

class Comment(db.Model):
    __tablename__ = "comments"
    __id = db.Column(db.String(16), primary_key=True, nullable=False)
    __card_id = db.Column(db.String(16), nullable=False)
    __user_id = db.Column(db.String(16), nullable=False)
    __reply_id = db.Column(db.String(16), nullable=True)
    __comment_content = db.Column(db.Text, nullable=False)
    __time = db.Column(db.Float,nullable = False)
    #------>发布卡片的部分
    def comment_on_card(self, comment_card_dict):
        '''示例：newcomment_dict{'card_id':'67687',
                                'user_id':'787897',
                                'to_user_id':'79980980',
                                'commtent_content':'真的有点很烦呢。'}'''

        self.__id = str(uuid.uuid1()).split("-")[0]
        self.__card_id = comment_card_dict['card_id']
        self.__user_id = comment_card_dict['user_id']
        self.__comment_content = comment_card_dict['content']
        self.set_reply_id(comment_card_dict)
        self.__time = time.time()

        return True

    def set_reply_id(self,dict):
        if dict['to_author']:
            self.__reply_id = None
        else:
            self.__reply_id = dict['reply_id']

    def check_data(self, user_id, data_dict):
        try:
            if not data_dict['content'] or \
                    not data_dict['card_id'] or \
                    not data_dict['user_id'] :
                raise PetLog_DataError(
                    'One comment card lack something')
                data_dict['reply_id']
                data_dict['to_author']
        except PetLog_DataError as error:
            print('Error : ' + error.message)
        except KeyError as error:
            print("KeyError : Don't has " + error)
        else:
            return data_dict

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return True

    #------->删除评论功能（是否能？）
    def delete(self, comment_id):
        comm = self.query.filter_by(_id=comment_id).first()
        db.session.delete(comm)
        db.session.commit()
        return True
    
    def get_time(self):
        return self.__time

    def get_tm_date(self):
        year = time.localtime(self.get_time()).tm_year
        mou = time.localtime(self.get_time()).tm_mon
        day = time.localtime(self.get_time()).tm_mday
        if year is time.localtime(time.time()).tm_year:
            return mou + '-' + day
        else:
            return year + '-' + mou + '-' + day
    
    def get_comments_with_card_number(self,card_id):
        return len(Comment.query.filter(Comment.__card_id == card_id).all())