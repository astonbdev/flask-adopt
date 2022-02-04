"""Forms for adopt app."""


from smtplib import SMTPRecipientsRefused
from flask_wtf import FlaskForm
from wtforms import StringField, Optional


class PetForm(FlaskForm):

    name = StringField("""validators""")

    species = StringField()

    photo_url = StringField(validators=[Optional()])

    age = StringField()

    notes = StringField(validators=[Optional()])


