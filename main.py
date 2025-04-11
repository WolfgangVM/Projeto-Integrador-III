from flask import Flask
from extensions import db, bcrypt, login_manager
from app.auth.login_routes import login_bp
from app.auth.signup_routes import signup_bp
from app.auth.forgot_password_routes import forgot_password_bp
from app.system.system_routes import system_bp
from data.users import users_bp
import os

app = Flask(__name__, template_folder='app/layout/templates', static_folder='app/layout/static')
app.secret_key = '3c1b41c7b50912966d49ae4a198a6a3913a76c930e9ef38e'
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {
        'check_same_thread': False
    }
}
app.config['LOGIN_VIEW'] = 'login.login'  
app.config['LOGIN_MESSAGE'] = 'Por favor, faça login para acessar essa página.'
app.config['LOGIN_MESSAGE_CATEGORY'] = 'info'
app.config['WTF_CSRF_ENABLED'] = True


db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)


app.register_blueprint(system_bp)
app.register_blueprint(forgot_password_bp)
app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(users_bp)

with app.app_context():
    if not os.path.exists('instance/site.db'):
        db.create_all()
        print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    app.run(debug=True)