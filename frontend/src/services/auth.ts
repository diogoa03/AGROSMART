import axios from 'axios';

const API_URL = 'http://localhost:5000/api/login';

export async function login(username: string, password: string) {
    const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
            'Authorization': 'Basic ' + btoa(username + ':' + password),
        },
    });
    if (!response.ok) throw new Error('Login failed');
    
    localStorage.setItem('token', btoa(username + ':' + password));
}

export const isAuthenticated = () => {
    return !!localStorage.getItem('token');
};

export const logout = () => {
    localStorage.removeItem('token');
};