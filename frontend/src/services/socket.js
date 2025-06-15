import io from 'socket.io-client';

const SOCKET_SERVER_URL = 'http://localhost:5000';

class SocketService {
    constructor() {
        this.socket = null;
        this.listeners = {};
    }

    // Inicializa a conexão socket
    connect() {
        if (!this.socket) {
            this.socket = io(SOCKET_SERVER_URL);
            console.log('Socket connected to server');
        }
        return this.socket;
    }

    // Desconecta o socket
    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
            this.socket = null;
            console.log('Socket disconnected from server');
        }
    }

    // Adiciona um listener para um evento específico
    on(event, callback) {
        if (!this.socket) {
            this.connect();
        }
        
        // Guarda referência ao callback para poder removê-lo depois
        if (!this.listeners[event]) {
            this.listeners[event] = [];
        }
        this.listeners[event].push(callback);
        
        // Adiciona o listener ao socket
        this.socket.on(event, callback);
        
        return () => this.off(event, callback);
    }

    // Remove um listener específico
    off(event, callback) {
        if (this.socket && callback) {
            this.socket.off(event, callback);
            
            // Remove da lista de listeners
            if (this.listeners[event]) {
                this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
            }
        }
    }

    // Emite um evento
    emit(event, data) {
        if (!this.socket) {
            this.connect();
        }
        this.socket.emit(event, data);
    }
}

// Singleton para garantir apenas uma instância de socket
const socketService = new SocketService();

export default socketService;