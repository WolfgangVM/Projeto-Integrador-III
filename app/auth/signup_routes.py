



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
