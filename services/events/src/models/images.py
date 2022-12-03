from models import db


class Image(db.Model):
    __tablename__ = 'images'

    event_id = db.Column(db.Integer, db.ForeignKey(
        'events.event_id'), primary_key=True)
    image = db.Column(db.String(50), nullable=False, primary_key=True)

    def __init__(self, event_id, image):
        self.event_id = event_id
        self.image = image

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "image": self.image
        }