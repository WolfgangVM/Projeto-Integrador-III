from flask import Blueprint, render_template, request, abort, redirect, url_for, flash
from flask_login import login_required, current_user
import requests
from deep_translator import GoogleTranslator
import re  # Biblioteca para limpeza de texto
import logging  # Import logging module

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

home_bp = Blueprint('home', __name__)

user_shelf = {}  # Temporary in-memory storage for user shelves

@home_bp.route("/home")
@login_required
def homepage():
    return render_template("home.html")

@home_bp.route("/about")
@login_required
def about():
    return render_template("about.html")

@home_bp.route("/privacy-policy")
@login_required
def privacy_policy():
    return render_template("privacy-policy.html")

@home_bp.route("/terms-use")
@login_required
def terms_use():
    return render_template("terms-use.html")

@home_bp.route("/help")
@login_required
def help_page():
    return render_template("help.html")

@home_bp.route("/contact")
@login_required
def contact_page():
    return render_template("contact.html")

@home_bp.route("/categories")
@login_required
def categories():
    return render_template("categories.html")

@home_bp.route("/categories/<string:category_name>")
@login_required
def category_page(category_name):
    BASE_URL = "https://www.googleapis.com/books/v1/volumes"
    page = request.args.get("page", 1, type=int)  # Obter o número da página da query string
    max_results = 40  # Reduzir para 40 livros por página (limite da API)
    start_index = (page - 1) * max_results

    params = {
        "q": category_name,
        "maxResults": max_results,
        "startIndex": start_index
    }

    books_data = []
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        data = response.json()
        books = data.get("items", [])

        for book in books:
            book_id = book.get("id", "ID não disponível")
            title = book["volumeInfo"].get("title", "Título não disponível")
            authors = book["volumeInfo"].get("authors", ["Autor não disponível"])
            cover_url = book["volumeInfo"].get("imageLinks", {}).get("thumbnail", None)

            books_data.append({
                "id": book_id,
                "title": title,
                "authors": ", ".join(authors),
                "cover_url": cover_url
            })

        total_items = data.get("totalItems", 0)
        total_pages = (total_items + max_results - 1) // max_results  # Calcular o total de páginas
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao buscar livros para a categoria {category_name}: {e}")
        abort(500)
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")
        abort(500)

    return render_template(
        f"categories/{category_name}.html",
        category_name=category_name,
        books=books_data,
        current_page=page,
        total_pages=total_pages
    )

@home_bp.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":
        search_query = request.form.get("search-form")

        if not search_query or not search_query.strip():
            message = "O campo de pesquisa não pode estar vazio."
            return render_template("search.html", message=message)

        BASE_URL = "https://www.googleapis.com/books/v1/volumes"
        params = {
            "q": search_query.strip(),
            "maxResults": 20,
            "startIndex": 0
        }

        found_books = False
        books_data = []

        while True:
            try:
                response = requests.get(BASE_URL, params=params)
                response.raise_for_status()

                data = response.json()
                books = data.get("items", [])

                if not books:
                    break

                found_books = True

                for book in books:
                    title = book["volumeInfo"].get("title", "Título não disponível")
                    description = book["volumeInfo"].get("description", "")
                    categories = book["volumeInfo"].get("categories", [])
                    authors = book["volumeInfo"].get("authors", ["Autor não disponível"])
                    cover_url = book["volumeInfo"].get("imageLinks", {}).get("thumbnail", None)

                    # Filtrar livros que tenham relação com a consulta
                    if search_query.lower() in title.lower() or \
                       search_query.lower() in description.lower() or \
                       any(search_query.lower() in category.lower() for category in categories):
                        books_data.append({
                            "id": book.get("id"),
                            "title": title,
                            "authors": ", ".join(authors),
                            "cover_url": cover_url
                        })

                params["startIndex"] += len(books)
            except requests.exceptions.RequestException as e:
                print(f"Erro ao se comunicar com a API: {e}")
                message = "Ocorreu um erro ao buscar os livros. Tente novamente mais tarde."
                return render_template("search_results.html", query=search_query, books=[], message=message)

        if not found_books:
            message = "Nenhum livro foi encontrado para a pesquisa."
            return render_template("search_results.html", query=search_query, books=[], message=message)

        return render_template("search_results.html", query=search_query, books=books_data)

    return render_template("search.html")

def translate_text(text, target_language="pt"):
    """
    Divide o texto em partes menores e traduz cada parte separadamente.
    """
    translator = GoogleTranslator(source='auto', target=target_language)
    max_length = 500  # Limite de caracteres por tradução
    parts = [text[i:i + max_length] for i in range(0, len(text), max_length)]
    translated_parts = [translator.translate(part) for part in parts]
    return " ".join(translated_parts)

@home_bp.route("/book/<string:book_id>")
@login_required
def book_details(book_id):
    BASE_URL = f"https://www.googleapis.com/books/v1/volumes/{book_id}"
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()

        book = response.json()
        if not book:
            abort(404)

        # Obter e limpar a descrição
        description = book["volumeInfo"].get("description", "Descrição não disponível")
        if description != "Descrição não disponível":
            # Remover caracteres especiais e normalizar o texto
            description = re.sub(r"[^\w\s.,;!?\"'´`-]", "", description)
            description = translate_text(description)

        # Traduzir os gêneros para português, se disponíveis
        genres = book["volumeInfo"].get("categories", ["Gênero não disponível"])
        translated_genres = [translate_text(genre) for genre in genres]

        # Obter o link para leitura completa, se disponível
        full_access_url = book["accessInfo"].get("webReaderLink", None)

        # Garantir que o ID do livro está incluído
        book_data = {
            "id": book_id,
            "title": book["volumeInfo"].get("title", "Título não disponível"),
            "authors": ", ".join(book["volumeInfo"].get("authors", ["Autor não disponível"])),
            "description": description,
            "genre": ", ".join(translated_genres),
            "year": book["volumeInfo"].get("publishedDate", "Ano não disponível"),
            "cover_url": book["volumeInfo"].get("imageLinks", {}).get("thumbnail", None),
            "full_access_url": full_access_url,
        }

        # Verificar se o livro já está na estante do usuário
        user_books = user_shelf.get(current_user.id, [])
        book_in_shelf = any(book["id"] == book_id for book in user_books)

        return render_template("book_details.html", book=book_data, book_in_shelf=book_in_shelf)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar detalhes do livro: {e}")
        abort(500)

@home_bp.route("/shelf/add/<string:book_id>", methods=["POST"])
@login_required
def add_to_shelf(book_id):
    # Obter os dados do formulário
    book_data = {
        "id": request.form.get("id"),
        "title": request.form.get("title"),
        "authors": request.form.get("authors"),
        "cover_url": request.form.get("cover_url"),
    }

    # Log para depuração
    print(f"Dados recebidos do formulário: {book_data}")

    # Verificar se o ID do livro está presente
    if not book_data["id"]:
        flash("Erro: ID do livro não encontrado.")
        return redirect(url_for("home.shelf"))

    # Obter a estante do usuário atual
    user_books = user_shelf.setdefault(current_user.id, [])

    # Verificar se o livro já está na estante
    if any(book["id"] == book_id for book in user_books):
        flash(f"O livro '{book_data.get('title', 'Desconhecido')}' já está na sua estante.")
    else:
        user_books.append(book_data)
        flash(f"O livro '{book_data.get('title', 'Desconhecido')}' foi adicionado à sua estante.")

    # Log para verificar o estado da estante
    print(f"Estante do usuário {current_user.id}: {user_books}")

    return redirect(url_for("home.shelf"))

@home_bp.route("/shelf/remove/<string:book_id>", methods=["POST"])
@login_required
def remove_from_shelf(book_id):
    user_books = user_shelf.get(current_user.id, [])
    updated_books = [book for book in user_books if book["id"] != book_id]

    if len(updated_books) < len(user_books):
        user_shelf[current_user.id] = updated_books
        flash("O livro foi removido da sua estante.")
    else:
        flash("Erro: O livro não foi encontrado na sua estante.")

    return redirect(url_for("home.shelf"))

@home_bp.route("/shelf")
@login_required
def shelf():
    books = user_shelf.get(current_user.id, [])
    return render_template("shelf.html", books=books)

