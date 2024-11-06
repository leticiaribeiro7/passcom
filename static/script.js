document.getElementById('register-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const uuid = document.getElementById('uuid').value;

    const requestData = {
        username: username,
        password: password,
        uuid: uuid
    };

    const portaServidor = localStorage.getItem("portaServidor");

    try {
        const response = await fetch(`http://localhost:${portaServidor}/register-all`, {
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
