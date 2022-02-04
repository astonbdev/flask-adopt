from flask import Flask, render_template, flash, redirect

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Pet

from forms import PetForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

@app.get('/')
def show_homepage():
    """Display homepage"""

    pets = Pet.query.all()
    return render_template("home.html", pets=pets)

@app.route('/add', methods=["GET", "POST"])
def show_add_pet_form():
    """displays and processes form POST request for adding a pet"""

    pet_form = PetForm()

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
    pet_form = PetForm(obj=pet)

    if pet_form.validate_on_submit():

        pet.name = pet_form.name.data
        pet.species = pet_form.species.data
        pet.photo_url = pet_form.photo_url.data
        pet.age = pet_form.age.data
        pet.notes = pet_form.notes.data

        db.session.commit()
        flash(f"Edited {pet.name}!")
        return redirect(f"/{pet_id}")

    else:
       return render_template("pet_info.html", pet=pet, form=pet_form)