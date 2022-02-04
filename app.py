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
def add_pet():

    pet_form = PetForm()

    if pet_form.validate_on_submit():
        
        pet = Pet(
            name=pet_form.name.data,
            species=pet_form.species.data,
            photo_url=pet_form.photo_url.data,
            age=pet_form.age.data,
            notes=pet_form.notes.data)
        db.session.add(pet)
        db.session.commit()
        flash(f"Add {pet.name}!")
        return redirect("/")
    
    else: 
        return render_template("add_pet.html", form=pet_form)