document.addEventListener('DOMContentLoaded', () => {
    const livros = [
        { nome: 'Dom Quixote', tema: 'Aventura' },
        { nome: '1984', tema: 'Ficção Científica' },
        { nome: 'O Senhor dos Anéis', tema: 'Fantasia' },
        { nome: 'Cem Anos de Solidão', tema: 'Realismo Mágico' }
    ];

    const buscaNomeInput = document.getElementById('buscaNome');
    const buscaTemaInput = document.getElementById('buscaTema');
    const btnBuscar = document.getElementById('btnBuscar');
    const listaLivros = document.getElementById('listaLivros');

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
        resultados.forEach(livro => {
            const itemLista = document.createElement('li');
            itemLista.textContent = `${livro.nome} - ${livro.tema}`;
            listaLivros.appendChild(itemLista);
        });
    }
});