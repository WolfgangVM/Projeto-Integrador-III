





# Rotas

@app.route("/")    
@login_required     # Requer que o usuário esteja logado para acessar esta rota 
def homepage():         
    return render_template("index.html")    