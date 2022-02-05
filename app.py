from urllib import response

import os

from flask import Flask, render_template, flash, redirect

import requests

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Pet

from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

PET_API_KEY = os.environ['PET_API_KEY']
PET_API_SECRET = os.environ['PET_API_SECRET']
ACCESS_TOKEN = ""

connect_db(app)
db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

@app.before_first_request
def refresh_credentials():
    """Gets OAuth token from PetFinder API"""
    update_auth_token_string()


@app.get('/')
def show_homepage():
    """Display homepage"""
    breakpoint()
    pets = Pet.query.all()
    return render_template("home.html", pets=pets)

@app.route('/add', methods=["GET", "POST"])
def show_add_pet_form():
    """displays and processes form POST request for adding a pet"""

    pet_form = AddPetForm()

    if pet_form.validate_on_submit():

        pet = Pet(
            name=pet_form.name.data,
            species=pet_form.species.data,
            photo_url=pet_form.photo_url.data,
            age=pet_form.age.data,
            notes=pet_form.notes.data
        )

        db.session.add(pet)
        db.session.commit()
        flash(f"Added {pet.name}!")
        return redirect("/")

    else:
        return render_template("add_pet.html", form=pet_form)

@app.route('/<int:pet_id>', methods=["GET", "POST"])
def show_pet_info_form(pet_id):
    """displays pet info page, and also processes
       form POST requests to edit pet info"""

    pet = Pet.query.get_or_404(pet_id)
    pet_form = EditPetForm(obj=pet)

    if pet_form.validate_on_submit():

        pet.photo_url = pet_form.photo_url.data
        pet.notes = pet_form.notes.data
        pet.available = pet_form.available.data

        db.session.commit()
        flash(f"Edited {pet.name}!")
        return redirect(f"/{pet_id}")

    else:
       return render_template("pet_info.html", pet=pet, form=pet_form)


def update_auth_token_string():

    resp = requests.get(
        "https://api.petfinder.com/v2/oauth2/token",
        data={
            "grant_type": "client_credentials",
            "client_id": PET_API_KEY,
            "client_secret": PET_API_SECRET
        }
    )

    global ACCESS_TOKEN
    ACCESS_TOKEN = resp.json()