from models import db

from hashlib import sha1


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.String(30), unique=True, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(8), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(30), nullable=False)

    def __init__(self, employee_id, name, phone_number, email, password, role):
        self.employee_id = employee_id
        self.name = name
        self.phone_number = phone_number
        self.password = sha1(password.encode('utf-8')).hexdigest()
        self.email = email
        self.role = role

    def to_dict(self):
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "role": self.role,
        }
