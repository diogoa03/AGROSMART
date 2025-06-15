// Define o endereço base para autenticação na API
const API_URL = 'http://localhost:5000/api/login';



//Função que realiza a autenticação do utilizador na API
export async function login(username, password) {

    // Faz um pedido POST ao servidor para autenticar o utilizador
    const response = await fetch(API_URL, {

        method: 'POST', 
        headers: {
            // Codifica as credenciais em Base64 no formato "Basic Authentication"
            'Authorization': 'Basic ' + btoa(username + ':' + password),
        },
    });
    
    // Se a resposta não for bem-sucedida, lança um erro
    if (!response.ok) throw new Error('Login failed');
    
    // Guarda o token de autenticação no armazenamento local do navegador
    // para manter o utilizador autenticado entre visitas
    localStorage.setItem('token', btoa(username + ':' + password));
}


 //Verifica se o utilizador está autenticado

export const isAuthenticated = () => {
    // Verifica se existe um token guardado no armazenamento local
    return !!localStorage.getItem('token');
};


 //Termina a sessão do utilizador
export const logout = () => {
    // Remove o token do armazenamento local, desautenticando o utilizador
    localStorage.removeItem('token');
};