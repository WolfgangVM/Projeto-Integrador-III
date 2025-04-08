from flask import Flask
from extensions import db, bcrypt, login_manager
from app.auth.login_routes import login_bp
from app.auth.signup_routes import signup_bp
from data.users import users_bp

app = Flask(__name__, template_folder='app/layout/templates', static_folder='app/layout/static')
app.secret_key = '3c1b41c7b50912966d49ae4a198a6a3913a76c930e9ef38e'
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Inicializar extensões
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

# Registrar blueprints
app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(users_bp)

if __name__ == "__main__":
    app.run(debug=True)