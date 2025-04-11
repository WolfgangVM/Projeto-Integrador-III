from flask import Blueprint, jsonify

system_bp = Blueprint('system', __name__)

@system_bp.route('/api/livros', methods=['GET'])
def get_livros():
    livros = [
        {'nome': 'Dom Quixote', 'tema': 'Aventura'},
        {'nome': '1984', 'tema': 'Ficção Científica'},
        {'nome': 'O Senhor dos Anéis', 'tema': 'Fantasia'},
        {'nome': 'Cem Anos de Solidão', 'tema': 'Realismo Mágico'}
    ]
    return jsonify(livros)