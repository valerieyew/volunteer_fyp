from models import db

from datetime import datetime


class Session(db.Model):
    __tablename__ = 'sessions'

    session_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey(
        'events.event_id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    capacity = db.Column(db.Integer, nullable=False)
    fill = db.Column(db.Integer, nullable=False)

    def __init__(self, session_id, event_id, start_time, end_time,
                 capacity, fill):
        self.session_id = session_id
        self.event_id = event_id
        self.start_time = start_time
        self.end_time = end_time
        self.capacity = capacity
        self.fill = fill

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "event_id": self.event_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "capacity": self.capacity,
            "fill": self.fill
        }
