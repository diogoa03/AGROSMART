import React, { useState } from 'react';

interface LoginFormProps {
    onLogin: (username: string, password: string) => Promise<void>;
}

const LoginForm: React.FC<LoginFormProps> = ({ onLogin }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!username || !password) {
            setError('Please enter both username and password');
            return;
        }

        setIsSubmitting(true);
        setError('');

        try {
            await onLogin(username, password);
        } catch (err) {
            setError('Invalid username or password');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <form className="login-form" onSubmit={handleSubmit}>
            <div className="form-group">
                <label htmlFor="username">Username</label>
                <input
                    id="username"
                    type="text"
                    className="form-control"
                    placeholder="Username"
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                    disabled={isSubmitting}
                />
            </div>
            <div className="form-group">
                <label htmlFor="password">Password</label>
                <input
                    id="password"
                    type="password"
                    className="form-control"
                    placeholder="Password"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    disabled={isSubmitting}
                />
            </div>
            {error && <div className="error-message">{error}</div>}
            <button 
                type="submit" 
                className="login-btn"
                disabled={isSubmitting}
            >
                {isSubmitting ? 'Logging in...' : 'Login'}
            </button>
        </form>
    );
};

export default LoginForm;