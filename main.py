from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#usado para banco de dados, se não usar deixar comentado
#flask sqlalchemy

#usado para formularios, se não usar deixar comentado
#flask wtf forms

app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Inicializações
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from views import *

if __name__ == "__main__":
    app.run(debug=True)
