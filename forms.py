"""Forms for adopt app."""


from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, ValidationError
from wtforms.validators import Optional, InputRequired, URL

def validate_species(form, field):
    """Validates species from defined list, uses wtforms validators"""

    species_list = ["cat", "dog", "porcupine"]
    if field.data.lower() not in species_list:
        raise ValidationError("Species not valid")

def validate_age(form, field):
    """Validates age from defined list, uses wtforms validators"""

    age_list = ["baby", "young", "adult", "senior"]
    if field.data.lower() not in age_list:
        raise ValidationError("Age not valid")

class AddPetForm(FlaskForm):
    """Form class for adding a pet"""

    name = StringField("Name", validators=[InputRequired()])

    species = StringField("Species", validators=[InputRequired(), validate_species])

    photo_url = StringField("Photo", validators=[Optional(), URL()])

    age = StringField("Age", validators=[InputRequired(), validate_age])

    notes = StringField("Notes", validators=[Optional()])

class EditPetForm(FlaskForm):
    """Form class for editing a pet"""

    photo_url = StringField("Photo", validators=[Optional(), URL()])

    notes = StringField("Notes", validators=[Optional()])

    available = BooleanField("Availability", validators=[Optional()])




