from main import app, db, bcrypt    # Importando o aplicativo Flask, banco de dados e Bcrypt do arquivo main.py
from flask import render_template, redirect, url_for, flash, request    
from flask_login import login_user, logout_user, login_required, current_user   
from models import User 

# Rotas

@app.route("/")    
@login_required     # Requer que o usuário esteja logado para acessar esta rota 
def homepage():         
    return render_template("index.html")        

@app.route("/register", methods=["GET", "POST"])    # Rota para registro de novos usuários
def register():
    if request.method == "POST":    # Se o método da requisição for POST, significa que o formulário foi enviado
        username = request.form.get("username")    
        password = request.form.get("password")    
        if User.query.filter_by(username=username).first():    # Verifica se o nome de usuário já existe no banco de dados
            flash("Nome de usuário já existe. Tente outro.", "danger")
            return redirect(url_for("register"))       
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')   # Faz o hash da senha usando Bcrypt
        user = User(username=username, password=hashed_password)        # Cria uma nova instância do modelo User com o nome de usuário e senha hasheada
        db.session.add(user)       
        db.session.commit()     
        flash("Conta criada com sucesso!", "success")           # Exibe uma mensagem de sucesso
        return redirect(url_for("login"))      
    return render_template("register.html")         # Renderiza o template de registro se o método da requisição for GET

@app.route("/login", methods=["GET", "POST"])               # Rota para login de usuários
def login():                                                        
    if request.method == "POST":        # Se o método da requisição for POST, significa que o formulário foi enviado
        username = request.form.get("username")                    
        password = request.form.get("password")         
        user = User.query.filter_by(username=username).first()           
        if user and bcrypt.check_password_hash(user.password, password):        # Verifica se o usuário existe e se a senha informada confere com a senha hasheada no banco de dados
            login_user(user)
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("homepage"))        # Redireciona para a página inicial após o login
        else:                  # Se o usuário não existir ou a senha estiver incorreta
            flash("Falha no login. Verifique seu usuário e senha.", "danger")
    return render_template("login.html")

@app.route("/logout")        # Rota para logout de usuários
@login_required         
def logout():                               
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("login"))