from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from extensions import db, bcrypt
from data.users import User

login_bp = Blueprint('login', __name__)

@login_bp.route("/")
def login():
    return render_template("login.html")

@login_bp.route("/register")
def register():
    return render_template("register.html")

@login_bp.route("/forgot_password")
def forgot_password():
    return render_template("forgot_password.html")

@login_bp.route("/home")
def home():
    return render_template("home.html")

@login_bp.route("/login", methods=["GET", "POST"])
def process_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("login.homepage"))
        else:
            flash("Falha no login. Verifique seu usuário e senha.", "danger")
    return render_template("login.html")

@login_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("login.login"))