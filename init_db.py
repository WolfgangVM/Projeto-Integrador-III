from main import app, db

# Inicializar o banco de dados
with app.app_context():
    db.create_all()
    print("Banco de dados inicializado com sucesso!")