from project import db


class Tag_with_Card(db.Model):
    __tablename__ = "Tag_with_Card"
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, nullable=False)
    card_id = db.Column(db.String(16), nullable=False)

    def create_tag_with_card(self, card_id, tag_id_list):
        for t in tag_id_list:
            tc = Tag_with_Card()
            tc.tag_id = t
            tc.card_id = card_id
            db.session.add(tc)
        db.session.commit()
        return True

    def get_cid_with_tid(tag_id):
        all = Tag_with_Card.query.filter(Tag_with_Card.tag_id == tag_id).all()
        if all:
            cards_id = []
            for one in all:
                cards_id.append(one.card_id)
            return cards_id
        else:
            return []

    def get_tid_with_cid(card_id):
        all = Tag_with_Card.query.filter(
            Tag_with_Card.card_id == card_id).all()
        if all:
            tags_id = []
            for one in all:
                tags_id.append(one.tag_id)
            return tags_id
        else:
            return []
