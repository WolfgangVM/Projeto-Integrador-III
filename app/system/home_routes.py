from flask import Blueprint, render_template, request, abort
from flask_login import login_required
import requests

home_bp = Blueprint('home', __name__)

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
    params = {
        "q": category_name,
        "maxResults": 40,
        "startIndex": 0
    }

    books_data = []
    while True:
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()

            data = response.json()
            books = data.get("items", [])

            if not books:
                break

            for book in books:
                title = book["volumeInfo"].get("title", "Título não disponível")
                authors = book["volumeInfo"].get("authors", ["Autor não disponível"])
                cover_url = book["volumeInfo"].get("imageLinks", {}).get("thumbnail", None)

                books_data.append({
                    "title": title,
                    "authors": ", ".join(authors),
                    "cover_url": cover_url
                })

            params["startIndex"] += len(books)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar livros para a categoria {category_name}: {e}")
            abort(500)

    return render_template(f"categories/{category_name}.html", category_name=category_name, books=books_data)

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
                    authors = book["volumeInfo"].get("authors", ["Autor não disponível"])
                    cover_url = book["volumeInfo"].get("imageLinks", {}).get("thumbnail", None)

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

        book_data = {
            "title": book["volumeInfo"].get("title", "Título não disponível"),
            "authors": ", ".join(book["volumeInfo"].get("authors", ["Autor não disponível"])),
            "description": book["volumeInfo"].get("description", "Descrição não disponível"),
            "genre": ", ".join(book["volumeInfo"].get("categories", ["Gênero não disponível"])),
            "year": book["volumeInfo"].get("publishedDate", "Ano não disponível"),
            "cover_url": book["volumeInfo"].get("imageLinks", {}).get("thumbnail", None),
        }

        return render_template("book_details.html", book=book_data)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar detalhes do livro: {e}")
        abort(500)