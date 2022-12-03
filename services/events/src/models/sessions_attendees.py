from models import db


class Session_Attendee(db.Model):
    __tablename__ = 'sessions_attendees'

    session_id = db.Column(db.Integer, db.ForeignKey(
        'sessions.session_id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey(
        'events.event_id'), nullable=False)
    employee_id = db.Column(db.String(30), nullable=False, primary_key=True)
    point = db.Column(db.String(50), nullable=False)

    def __init__(self, session_id, event_id, employee_id, point):
        self.session_id = session_id
        self.event_id = event_id
        self.employee_id = employee_id
        self.point = point

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "event_id": self.event_id,
            "employee_id": self.employee_id,
            "point": self.point
        }