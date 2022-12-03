from models import db


class Tag(db.Model):
    __tablename__ = 'tags'

    event_id = db.Column(db.Integer, db.ForeignKey(
        'events.event_id'), primary_key=True)
    tag = db.Column(db.String(50), nullable=False, primary_key=True)

    def __init__(self, event_id, tag):
        self.event_id = event_id
        self.tag = tag

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "tag": self.tag
        }