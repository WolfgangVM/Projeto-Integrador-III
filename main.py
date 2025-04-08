from flask import Flask                     
from flask_sqlalchemy import SQLAlchemy     
from flask_bcrypt import Bcrypt             
from flask_login import LoginManager
from app.auth.login_routes import login_bp    
from app.auth.signup_routes import signup_bp
from data.users import users_bp


app = Flask(__name__, template_folder='app/layout/templates', static_folder='app/layout/static')     
app.secret_key = '3c1b41c7b50912966d49ae4a198a6a3913a76c930e9ef38e'    

app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(users_bp)

app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'             
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'     

db = SQLAlchemy(app)                                            
bcrypt = Bcrypt(app)                                            
login_manager = LoginManager(app)                               
login_manager.login_view = 'login'                              
           
if __name__ == "__main__":                
    app.run(debug=True)                
