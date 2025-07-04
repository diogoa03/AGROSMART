import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect, useLocation } from 'react-router-dom';
import LoginPage from './pages/LoginPage'; 
import RegisterPage from './pages/RegisterPage';  
import Sidebar from './components/layout/Sidebar';
import Recommendations from './components/weather/Recommendations';
import Notifications from './components/weather/Notifications';
import Weather from './components/weather/Weather';
import History from './components/weather/History';
import HomePage from './pages/HomePage';
import ContactPage from './pages/ContactPage';
import UserProfilePage from './pages/UserProfilePage'; 
import { isAuthenticated } from './services/auth';
import './styles/index.css';
import '@fortawesome/fontawesome-free/css/all.min.css';

// Componente para as rotas protegidas com sidebar
const AgrosmartLayout = () => {
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
          <Route path="/agrosmart/profile">
            <UserProfilePage />
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
const PrivateRoute = ({ children, ...rest }) => (
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

const App = () => {
  return (
    <Router>
      <div className="app-container">
        <Switch>
          <Route path="/" exact component={LoginPage} />
          <Route path="/register" exact component={RegisterPage} />
          <PrivateRoute path="/agrosmart">
            <AgrosmartLayout />
          </PrivateRoute>
          <Redirect to="/" />
        </Switch>
      </div>
    </Router>
  );
};

export default App;