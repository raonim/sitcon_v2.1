// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {

    // --- BLOCO 1: LÓGICA PARA O FORMULÁRIO DE CADASTRO ---
    const formCadastro = document.querySelector('form[action="/cadastro"]');
    if (formCadastro) {
        formCadastro.addEventListener('submit', function(event) {
            const senhaInput = document.getElementById('senha');
            const confirmarSenhaInput = document.getElementById('confirmar_senha');

            if (senhaInput.value !== confirmarSenhaInput.value) {
                alert('As senhas não conferem. Por favor, verifique.');
                event.preventDefault(); 
            }
        });
    }


    // --- BLOCO 2: LÓGICA PARA O MAPA (INDEPENDENTE DO BLOCO 1) ---
    const mapaContainer = document.getElementById('mapa-container');
    const mostrarMapaBtn = document.getElementById('mostrar-mapa-btn');

    // Se o botão do mapa e o container existirem nesta página...
    if (mostrarMapaBtn && mapaContainer) {
        
        // Adiciona um "ouvinte" para o evento de clique no botão
        mostrarMapaBtn.addEventListener('click', function() {
            
            // Pega a latitude e longitude dos atributos 'data-*' que definimos no HTML
            const lat = parseFloat(mapaContainer.dataset.lat);
            const lon = parseFloat(mapaContainer.dataset.lon);

            // Torna o container do mapa visível
            mapaContainer.style.display = 'block';
            
            // Insere o mapa do Google dentro do container usando um iframe
            mapaContainer.innerHTML = `
                <iframe
                  width="100%"
                  height="100%"
                  style="border:0"
                  loading="lazy"
                  allowfullscreen
                  referrerpolicy="no-referrer-when-downgrade"
                  src="https://www.google.com/maps?q=${lat},${lon}&hl=es;z=14&amp;output=embed">
                </iframe>
            `;

            // Esconde o botão para não criar vários mapas
            this.style.display = 'none';
        });
    }

});
