from project import db

class Tag(db.Model):
    __tablename__ ="tags"
    __id = db.Column(db.String(16),primary_key=True,nullable=False)
    __tag_name = db.Column(db.String(32),nullable=False)
    
    def all_tags(self):
        all_tag = self.query.all()
        all_content = []
        for nei in all_tag:
            all_content.append(nei['__tag_name'])
        return all_content
