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

@home_bp.route("/privacy-policy")
@login_required
def privacy_policy():
    return render_template("privacy-policy.html")

@home_bp.route("/terms-use")
@login_required
def terms_use():
    return render_template("terms-use.html")

@home_bp.route("/help")
@login_required
def help_page():
    return render_template("help.html")

@home_bp.route("/contact")
@login_required
def contact_page():
    return render_template("contact.html")