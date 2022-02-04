"""Models for adopt app."""

from email.policy import default
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)


class Pet(db.Model):
    """Pet"""

    __tablename__ = 'pets'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = db.Column(db.Text)

    species = db.Column(db.Text)

    photo_url = db.Column(db.Text, default="")

    age = db.Column(db.Text)

    notes = db.Column(db.Text, nullable=True)

    available = db.Column(db.Boolean, default=True)
