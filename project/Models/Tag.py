from project import db

class Tag(db.Model):
    __id = db.Column(db.String(16), primary_key=True, nullable=False)
    __content = db.Column(db.Text, nullable=True)