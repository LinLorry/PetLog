from project import db

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
        return Tag.query.filter(Tag.tag_name.in_(tag_name)).first()

    def get_name(tag_id):
        return Tag.query.filter(Tag.id.in_(tag_id)).first()