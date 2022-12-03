from models import db

from datetime import datetime


class Post(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_title = db.Column(db.String(100), nullable=False)
    post_message = db.Column(db.String(1000), nullable=False)
    event_id = db.Column(db.Integer, nullable=False)
    posted_by_id = db.Column(db.String(30), nullable=False)
    posted_by_name = db.Column(db.String(30), nullable=False)
    posted_on = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, post_id, post_title, post_message, event_id, posted_by_id, posted_by_name):
        self.post_id = post_id
        self.post_title = post_title
        self.post_message = post_message
        self.event_id = event_id
        self.posted_by_id = posted_by_id
        self.posted_by_name = posted_by_name
        
    def to_dict(self):
        return {
            "post_id": self.post_id,
            "post_title": self.post_title,
            "post_message": self.post_message,
            "event_id": self.event_id,
            "posted_by_id": self.posted_by_id,
            "posted_by_name": self.posted_by_name,
            "posted_on": self.posted_on
        }
