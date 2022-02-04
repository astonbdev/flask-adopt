"""Forms for adopt app."""


from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Optional


class PetForm(FlaskForm):

    name = StringField("Name")

    species = StringField("Species")

    photo_url = StringField("Photo")

    age = StringField("Age")

    notes = StringField("Notes")


