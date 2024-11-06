document.getElementById('register-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Impede o envio padrão do formulário

    // Coleta os dados do formulário
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const uuid = document.getElementById('uuid').value;

    // Prepara o corpo da requisição
    const requestData = {
        username: username,
        password: password,
        uuid: uuid
    };

    try {
        // Faz a requisição POST para a API
        const response = await fetch('/api/users/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const result = await response.json();

        if (response.ok) {
            alert('Cadastro realizado com sucesso!');
        } else {
            alert('Erro: ' + result.message);
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
        alert('Ocorreu um erro ao tentar realizar o cadastro.');
    }
});
