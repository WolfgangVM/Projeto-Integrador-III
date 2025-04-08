from main import app, db, bcrypt    
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from data.users import User


signup_bp = Blueprint('signup', __name__)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":    
        username = request.form.get("username")    
        password = request.form.get("password")    
        if User.query.filter_by(username=username).first():    
            flash("Nome de usuário já existe. Tente outro.", "danger")
            return redirect(url_for("register"))       
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')   
        user = User(username=username, password=hashed_password)        
        db.session.add(user)       
        db.session.commit()     
        flash("Conta criada com sucesso!", "success")           
        return redirect(url_for("login"))      
    return render_template("register.html")        

