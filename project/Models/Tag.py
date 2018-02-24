from project import db

class Tag(db.Model):
    __tablename__ ="Tags"
    __id = db.Column(db.String(16),primary_key=True,nullable=False)
    __tag_name = db.Column(db.String(32),nullable=False)
    
    ''' def __init__(self,tag_name = None,tag_id =None):
        if not tag_id :
            info = self.query.filter(Tag.__id == tag_id).first()
            self.__id = info.__id
            self.__tag_name = info.__tag_name
        elif not tag_name is None:
            info = self.query.filter(Tag.__tag_name = tag_name).first()
            self.__id = info.__id
            self.__tag_name = info.__tag_name '''

    def all_tags(self):
        all_tag = self.query.all()
        all_content = []
        for nei in all_tag:
            all_content.append(nei['__tag_name'])
        return all_content
    
    def get_id(tag_name):
        return Tag.query.filter(Tag.__tag_name.in_(tag_name)).first()

    def get_name(tag_id):
        return Tag.query.filter(Tag.__id.in_(tag_id)).first()