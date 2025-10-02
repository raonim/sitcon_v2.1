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



// --- BLOCO 2: LÓGICA CORRIGIDA PARA O MAPA ---
const mapaContainer = document.getElementById('mapa-container');
const mostrarMapaBtn = document.getElementById('mostrar-mapa-btn');

if (mostrarMapaBtn && mapaContainer) {
    mostrarMapaBtn.addEventListener('click', function() {
        const lat = parseFloat(mapaContainer.dataset.lat);
        const lon = parseFloat(mapaContainer.dataset.lon);

        mapaContainer.style.display = 'block';
        
        // A URL agora está dentro de crases (`) e as variáveis estão formatadas corretamente
        mapaContainer.innerHTML = `
            <iframe
              width="100%"
              height="100%"
              style="border:0"
              loading="lazy"
              allowfullscreen
              referrerpolicy="no-referrer-when-downgrade"
              src="https://maps.google.com/maps?q=${lat},${lon}&hl=es;z=18&amp;output=embed">
            </iframe>
        `;

        this.style.display = 'none';
    });
}

    
// --- BLOCO 3: CÓDIGO ATUALIZADO PARA O MENU SANFONA INDEPENDENTE ---
const accordionTitles = document.querySelectorAll('.grupo-titulo[data-target]');

accordionTitles.forEach(title => {
    title.addEventListener('click', function() {
        // Encontra o grupo de botões correspondente ao título clicado
        const targetId = this.getAttribute('data-target');
        const targetGroup = document.querySelector(targetId);

        // Simplesmente adiciona ou remove a classe 'active' no título (para girar a seta)
        this.classList.toggle('active');
        
        // E também adiciona ou remove a classe 'active' no grupo de botões (para a animação)
        targetGroup.classList.toggle('active');
    });
});

});