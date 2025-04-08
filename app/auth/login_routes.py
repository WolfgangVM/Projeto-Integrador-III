from main import app, db, bcrypt    
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from data.users import User


login_bp = Blueprint('login', __name__)

@app.route("/")
@login_required
def homepage():         
    return render_template("index.html")

@login_bp.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

@login_bp.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')
     
@app.route("/login", methods=["GET", "POST"])               
def login():                                                        
    if request.method == "POST":        
        username = request.form.get("username")                    
        password = request.form.get("password")         
        user = User.query.filter_by(username=username).first()           
        if user and bcrypt.check_password_hash(user.password, password):        
            login_user(user)
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("homepage"))        
        else:                  
            flash("Falha no login. Verifique seu usuário e senha.", "danger")
    return render_template("login.html")

@app.route("/logout")        
@login_required         
def logout():                               
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("login"))
