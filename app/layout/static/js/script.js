document.addEventListener('DOMContentLoaded', () => {
    const buscaNomeInput = document.getElementById('buscaNome');
    const buscaTemaInput = document.getElementById('buscaTema');
    const btnBuscar = document.getElementById('btnBuscar');
    const listaLivros = document.getElementById('listaLivros');

    let livros = [];


    fetch('/api/livros')
        .then(response => response.json())
        .then(data => {
            livros = data;
        })
        .catch(error => console.error('Erro ao buscar livros:', error));

    btnBuscar.addEventListener('click', () => {
        const nomeBusca = buscaNomeInput.value.toLowerCase();
        const temaBusca = buscaTemaInput.value.toLowerCase();

        const resultados = livros.filter(livro => {
            return livro.nome.toLowerCase().includes(nomeBusca) && livro.tema.toLowerCase().includes(temaBusca);
        });

        exibirResultados(resultados);
    });

    function exibirResultados(resultados) {
        listaLivros.innerHTML = '';
        if (resultados.length === 0) {
            listaLivros.innerHTML = '<li>Nenhum livro encontrado.</li>';
            return;
        }
        resultados.forEach(livro => {
            const itemLista = document.createElement('li');
            itemLista.textContent = `${livro.nome} - ${livro.tema}`;
            listaLivros.appendChild(itemLista);
        });
    }
});

setTimeout(() => {
    const flashMessages = document.querySelector('.flash-messages');
    if (flashMessages) {
        flashMessages.style.display = 'none';
    }
}, 5000);