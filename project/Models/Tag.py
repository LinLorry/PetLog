from project import db
from .PetLogDataError import PetLog_DataError

class Tag(db.Model):
    __tablename__ ="Tags"
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    name = db.Column(db.String(32),nullable=False)


    def all_tags(self):
        all_tag = self.query.all()
        all_content = []
        for nei in all_tag:
            all_content.append(nei.name)
        return all_content
    
    def get_id(tag_name):
        tag_id = Tag.query.filter(Tag.tag_name.in_(tag_name)).first().id
        if tag_id is None:
            raise PetLog_DataError("Don't have this tag name : " + tag_name)
        else:
            return tag_id

    def get_name(tag_id):
        tag_name =  Tag.query.filter(Tag.id.in_(tag_id)).first().name
        if tag_name is None:
            raise PetLog_DataError("Don't have this tag id : " + tag_id)
        else:
            return tag_name