from flask import Blueprint, render_template
from flask_login import login_required

home_bp = Blueprint('home', __name__)

@home_bp.route("/home")
@login_required
def homepage():
    return render_template("home.html")

@home_bp.route("/about")
@login_required
def about():
    return render_template("about.html")