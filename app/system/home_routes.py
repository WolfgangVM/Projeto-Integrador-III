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
        "q": category_name,  # Use the category name as the search query
        "maxResults": 40,    # Fetch up to 40 results per request (API limit)
        "startIndex": 0      # Start from the first result
    }

    books_data = []
    while True:
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors

            data = response.json()
            books = data.get("items", [])

            if not books:
                break  # Stop if no more books are returned

            for book in books:
                title = book["volumeInfo"].get("title", "Título não disponível")
                authors = book["volumeInfo"].get("authors", ["Autor não disponível"])
                cover_url = book["volumeInfo"].get("imageLinks", {}).get("thumbnail", None)

                books_data.append({
                    "title": title,
                    "authors": ", ".join(authors),
                    "cover_url": cover_url
                })

            # Increment the startIndex to fetch the next set of results
            params["startIndex"] += len(books)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar livros para a categoria {category_name}: {e}")
            abort(500)  # Return a 500 error if the API request fails

    return render_template(f"categories/{category_name}.html", category_name=category_name, books=books_data)

@home_bp.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":
        search_query = request.form.get("search-form")
        print(search_query)  # Debug: imprime a consulta de pesquisa

        # Validação do campo de pesquisa
        if not search_query or not search_query.strip():
            message = "O campo de pesquisa não pode estar vazio."
            return render_template("search.html", message=message)

        BASE_URL = "https://www.googleapis.com/books/v1/volumes"
        params = {
            "q": search_query.strip(),  # Remove espaços em branco desnecessários
            "maxResults": 20,
            "startIndex": 0
        }

        found_books = False
        books_data = []  # Lista para armazenar os resultados

        while True:
            try:
                response = requests.get(BASE_URL, params=params)
                response.raise_for_status()  # Lança uma exceção para códigos de erro HTTP

                data = response.json()
                books = data.get("items", [])

                if not books:
                    break

                found_books = True

                for book in books:
                    title = book["volumeInfo"].get("title", "Título não disponível")
                    authors = book["volumeInfo"].get("authors", ["Autor não disponível"])
                    cover_url = book["volumeInfo"].get("imageLinks", {}).get("thumbnail", None)
                    
                    # Adiciona os dados à lista
                    books_data.append({
                        "id": book.get("id"),
                        "title": title,
                        "authors": ", ".join(authors),
                        "cover_url": cover_url
                    })

                params["startIndex"] += len(books)
            except requests.exceptions.RequestException as e:
                # Loga o erro e exibe uma mensagem ao usuário
                print(f"Erro ao se comunicar com a API: {e}")
                message = "Ocorreu um erro ao buscar os livros. Tente novamente mais tarde."
                return render_template("search_results.html", query=search_query, books=[], message=message)

        if not found_books:
            message = "Nenhum livro foi encontrado para a pesquisa."
            return render_template("search_results.html", query=search_query, books=[], message=message)

        # Renderiza o template com os resultados
        return render_template("search_results.html", query=search_query, books=books_data)

    return render_template("search.html")

@home_bp.route("/book/<string:book_id>")
@login_required
def book_details(book_id):
    BASE_URL = f"https://www.googleapis.com/books/v1/volumes/{book_id}"
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()  # Lança uma exceção para códigos de erro HTTP

        book = response.json()
        if not book:
            abort(404)  # Retorna erro 404 se o livro não for encontrado

        # Extrai os detalhes do livro
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
        abort(500)  # Retorna erro 500 em caso de falha na comunicação com a API