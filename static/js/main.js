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

    // --- BLOCO 1.5: INICIALIZA FOCO DA SANFONA ---
    // Esta função garante que, ao carregar a página, os links dentro
    // das sanfonas colapsadas não sejam focáveis via 'Tab'.
    const allAccordionGroups = document.querySelectorAll('.amv-button-group');
    
    allAccordionGroups.forEach(group => {
        // Verifica se o grupo NÃO está ativo (colapsado) no carregamento
        if (!group.classList.contains('active')) {
            // Pega todos os links (botões) dentro dele
            const links = group.querySelectorAll('a');
            // E desativa o 'Tab' para todos eles
            links.forEach(link => {
                link.tabIndex = -1;
            });
        }
    });


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

        // --- INÍCIO DA MODIFICAÇÃO DE ACESSIBILIDADE ---
        
        // Verifica se a sanfona está expandida AGORA (depois do toggle)
        const isExpanded = targetGroup.classList.contains('active');
        
        // Pega todos os links (botões) dentro do grupo que foi clicado
        const links = targetGroup.querySelectorAll('a');
        
        // Atualiza o 'tabIndex' de todos os links
        links.forEach(link => {
            // Se estiver expandido, tabIndex = 0 (torna focável)
            // Se estiver colapsado, tabIndex = -1 (torna não-focável)
            link.tabIndex = isExpanded ? 0 : -1;
        });
        // --- FIM DA MODIFICAÇÃO DE ACESSIBILIDADE ---
    });
});

// Encontra os mesmos títulos que tornamos focáveis
const accessibleButtons = document.querySelectorAll('.grupo-titulo[role="button"]');

accessibleButtons.forEach(button => {
    // Adiciona um ouvinte para teclas
    button.addEventListener('keydown', function(event) {

        // Verifica se a tecla pressionada é 'Enter' ou 'Espaço'
        if (event.key === 'Enter' || event.key === ' ' || event.key === 'Spacebar') {

            // Impede a página de rolar (ação padrão do 'Espaço')
            event.preventDefault();

            // Simula um clique no elemento, o que aciona o seu BLOCO 3
            // (o código que abre/fecha a sanfona)
            this.click();
        }
    });
});

});