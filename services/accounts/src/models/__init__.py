from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .accounts import Account  # noqa
