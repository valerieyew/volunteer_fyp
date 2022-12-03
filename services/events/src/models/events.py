from models import db

from datetime import datetime


class Event(db.Model):
    __tablename__ = 'events'

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    proposal_details = db.Column(db.String(500), nullable=False)
    info = db.Column(db.String(700), nullable=False)
    registration_opens_on = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    registration_closes_on = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(15), nullable=False)
    comments = db.Column(db.String(700), nullable=False)
    last_admin_action_by = db.Column(db.String(30), nullable=False)

    def __init__(self, event_id, employee_id, name, location, proposal_details, info,
                 registration_opens_on, registration_closes_on, status, comments, last_admin_action_by):
        self.event_id = event_id
        self.employee_id = employee_id
        self.name = name
        self.location = location
        self.proposal_details = proposal_details
        self.info = info
        self.registration_opens_on = registration_opens_on
        self.registration_closes_on = registration_closes_on
        self.status = status
        self.comments = comments
        self.last_admin_action_by = last_admin_action_by

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "employee_id": self.employee_id,
            "name": self.name,
            "location": self.location,
            "proposal_details": self.proposal_details,
            "info": self.info,
            "registration_opens_on": self.registration_opens_on,
            "registration_closes_on": self.registration_closes_on,
            "status": self.status,
            "comments": self.comments,
            "last_admin_action_by": self.last_admin_action_by
        }
