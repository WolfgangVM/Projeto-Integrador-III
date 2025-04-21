import requests

# URL base da API
BASE_URL = "https://www.googleapis.com/books/v1/volumes"

# Nome do livro que você quer buscar
book_name = "senhor dos anéis"  # Substitua pelo nome do livro desejado

# Parâmetros iniciais da busca
params = {
    "q": book_name,  # Query para buscar pelo nome do livro
    "maxResults": 20,  # Reduzido para processar menos resultados por página
    "startIndex": 0  # Índice inicial
}

found_books = False  # Variável para verificar se algum livro foi encontrado

while True:
    # Fazendo a requisição
    response = requests.get(BASE_URL, params=params)

    # Verificando o status da resposta
    if response.status_code == 200:
        data = response.json()
        books = data.get("items", [])
        
        # Se não houver mais resultados, interrompe o loop
        if not books:
            break
        
        found_books = True  # Marca que pelo menos um livro foi encontrado
        
        # Processa apenas os campos necessários
        for book in books:
            title = book["volumeInfo"].get("title", "Título não disponível")
            authors = book["volumeInfo"].get("authors", ["Autor não disponível"])
            
            print(f"Título: {title}")
            print(f"Autores: {', '.join(authors)}")
            print("-" * 40)
        
        # Atualiza o índice inicial para a próxima página
        params["startIndex"] += len(books)  # Incrementa pelo número de livros retornados
    else:
        print(f"Erro: {response.status_code}, {response.text}")
        break

# Exibe mensagem se nenhum livro foi encontrado
if not found_books:
    print("Nenhum livro foi encontrado para a pesquisa.")
