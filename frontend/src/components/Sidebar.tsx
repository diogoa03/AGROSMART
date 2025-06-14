import React from 'react';
import { useHistory } from 'react-router-dom';
import { logout } from '../services/auth';

interface SidebarProps {
    isOpen: boolean;
    toggleSidebar: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, toggleSidebar }) => {
    const history = useHistory();

    const handleLogout = () => {
        logout();
        history.push('/');
    };

    const handleNavigation = (path: string) => {
        history.push(path);
        toggleSidebar();
    };

    return (
        <aside className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
            <div className="sidebar-header">
                <button className="close-button" onClick={toggleSidebar}>✕</button>
            </div>
            <nav>
                <ul>
                    <li onClick={() => handleNavigation('/dashboard')}>
                        <svg className="sidebar-icon" viewBox="0 0 24 24">
                            <path fill="currentColor" d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
                        </svg>
                        Início
                    </li>
                    <li onClick={() => handleNavigation('/dashboard/weather')}>
                        <svg className="sidebar-icon" viewBox="0 0 24 24">
                            <path fill="currentColor" d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96z"/>
                        </svg>
                        Meteorologia
                    </li>
                    <li onClick={() => handleNavigation('/dashboard/alerts')}>
                        <svg className="sidebar-icon" viewBox="0 0 24 24">
                            <path fill="currentColor" d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6v-5c0-3.07-1.63-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.64 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2zm-2 1H8v-6c0-2.48 1.51-4.5 4-4.5s4 2.02 4 4.5v6z"/>
                        </svg>
                        Alertas
                    </li>
                    <li onClick={() => handleNavigation('/dashboard/recommendations')}>
                        <svg className="sidebar-icon" viewBox="0 0 24 24">
                            <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm4.17-5.24l-1.1-1.1c.71-1.33.53-3.01-.59-4.13C13.79 8.84 12.9 8.5 12 8.5c-.03 0-.06.01-.09.01L13 9.6l-1.06 1.06-2.83-2.83L11.94 5 13 6.06l-.96.96c1.27-.01 2.53.47 3.5 1.44 1.42 1.42 1.74 3.49.93 5.2l1.11 1.11-1.41 1.99z"/>
                        </svg>
                        Recomendacao
                    </li>
                    <li onClick={() => handleNavigation('/dashboard/history')}>
                        <svg className="sidebar-icon" viewBox="0 0 24 24">
                            <path fill="currentColor" d="M13 3c-4.97 0-9 4.03-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42C8.27 19.99 10.51 21 13 21c4.97 0 9-4.03 9-9s-4.03-9-9-9zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z"/>
                        </svg>
                        Histórico
                    </li>
                    <li onClick={handleLogout} className="logout-item">
                        <svg className="sidebar-icon" viewBox="0 0 24 24">
                            <path fill="currentColor" d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/>
                        </svg>
                        Sair
                    </li>
                </ul>
            </nav>
        </aside>
    );
};

export default Sidebar;