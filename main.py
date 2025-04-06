from flask import Flask                     # Importando Flask
from flask_sqlalchemy import SQLAlchemy     # Importando SQLAlchemy
from flask_bcrypt import Bcrypt             # Importando Bcrypt para hash de senhas
from flask_login import LoginManager        # Importando LoginManager para gerenciar sessões de login


app = Flask(__name__)                      

# Configurações
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'             # Chave secreta para proteger sessões
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'     # URI do banco de dados SQLite

# Inicializações
db = SQLAlchemy(app)                                            # Inicializa o banco de dados
bcrypt = Bcrypt(app)                                            # Inicializa o Bcrypt para hash de senhas
login_manager = LoginManager(app)                               # Inicializa o LoginManager
login_manager.login_view = 'login'                              # Define a rota de login para redirecionamento

from views import *                 # Importando as rotas do arquivo views.py

if __name__ == "__main__":          # Verificando se o script está sendo executado diretamente      
    app.run(debug=True)             # Iniciando o servidor Flask em modo de depuração   
