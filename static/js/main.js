// Logica para validar o formulário de cadastro
document.addEventListener('DOMContentLoaded', function() {


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
});
