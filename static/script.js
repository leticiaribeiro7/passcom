document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const login = document.getElementById('login').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ login, password })
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        alert('Login realizado com sucesso!');
        window.location.href = '/rotas';
    } else {
        alert('Credenciais inválidas');
    }
});

// Lógica para buscar rotas
async function fetchRotas() {
    const token = localStorage.getItem('token');
    const response = await fetch('/all-trechos', {
        headers: { 'Authorization': `Bearer ${token}` }
    });

    if (response.ok) {
        const rotas = await response.json();
        const container = document.getElementById('rotas-container');
        rotas.forEach(rota => {
            const div = document.createElement('div');
            div.textContent = `Origem: ${rota.origem}, Destino: ${rota.destino}`;
            container.appendChild(div);
        });
    } else {
        alert('Erro ao buscar rotas');
    }
}

// Chama a função para buscar rotas quando a página carrega
if (window.location.pathname === '/rotas') {
    fetchRotas();
}
