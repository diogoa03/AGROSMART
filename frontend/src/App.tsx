import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect, useLocation } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import Sidebar from './components/Sidebar';
import Recommendations from './components/Recommendations';
import Notifications from './components/Notifications';
import Weather from './components/Weather';
import History from './components/History';
import HomePage from './pages/HomePage';
import ContactPage from './pages/ContactPage';
import { isAuthenticated } from './services/auth';
import './App.css';
import '@fortawesome/fontawesome-free/css/all.min.css';

// Componente para as rotas protegidas com sidebar
const DashboardLayout: React.FC = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const location = useLocation();

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="agrosmart">
      <Sidebar isOpen={isSidebarOpen} toggleSidebar={toggleSidebar} />
      
      <div className={`main-content ${isSidebarOpen ? 'sidebar-open' : ''}`}>
        <header className="header">
          <button className="menu-button" onClick={toggleSidebar}>
            ☰
          </button>
          <img src="/agrosmart-logo.svg" alt="AgroSmart" className="logo" height="200"/>
        </header>
        
        <Switch>
          <Route path="/agrosmart/recommendations">
            <Recommendations />
          </Route>
          <Route path="/agrosmart/alerts">
            <Notifications />
          </Route>
          <Route path="/agrosmart/history">
            <History />
          </Route>
          <Route path="/agrosmart/weather">
            <Weather />
          </Route>
          <Route path="/agrosmart/contact">
            <ContactPage />
          </Route>
          <Route path="/agrosmart" exact>
            <HomePage />
          </Route>
        </Switch>
      </div>
    </div>
  );
};

// Componente de rota privada
const PrivateRoute: React.FC<any> = ({ children, ...rest }) => (
  <Route
    {...rest}
    render={({ location }) =>
      isAuthenticated() ? (
        children
      ) : (
        <Redirect to={{ pathname: '/', state: { from: location } }} />
      )
    }
  />
);

const App: React.FC = () => {
  return (
    <Router>
      <div className="app-container">
        <Switch>
          <Route path="/" exact component={LoginPage} />
          <PrivateRoute path="/agrosmart">
            <DashboardLayout />
          </PrivateRoute>
          <Redirect to="/" />
        </Switch>
      </div>
    </Router>
  );
};

export default App;