from flask import Flask

#usado para banco de dados, se não usar deixar comentado
#flask sqlalchemy

#usado para formularios, se não usar deixar comentado
#flask wtf forms


app = Flask(__name__)

from views import *

if __name__ == "__main__":
    app.run(debug=True)
