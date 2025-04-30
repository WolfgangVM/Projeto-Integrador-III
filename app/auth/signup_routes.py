from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db, bcrypt
from data.users import User
from flask import current_app
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user, logout_user

signup_bp = Blueprint('signup', __name__)

@signup_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("As senhas não coincidem. Tente novamente.", "danger")
            return redirect(url_for("signup.signup"))

        if len(password) < 6 or not any(c.isupper() for c in password) or not any(c in "!@#$%^&*" for c in password):
            flash("A senha deve ter pelo menos 6 caracteres, uma letra maiúscula e um caractere especial.", "danger")
            return redirect(url_for("signup.signup"))

        if User.query.filter_by(username=username).first():
            flash("Nome de usuário já existe. Tente outro.", "danger")
            return redirect(url_for("signup.signup"))

        if User.query.filter_by(email=email).first():
            flash("E-mail já cadastrado. Tente outro.", "danger")
            return redirect(url_for("signup.signup"))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Conta criada com sucesso!", "success")
        return redirect(url_for("login.loginpage"))

    return render_template("signup.html")