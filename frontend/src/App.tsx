import React from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import { isAuthenticated } from './services/auth';
import './App.css';

const PrivateRoute: React.FC<any> = ({ component: Component, ...rest }) => (
  <Route
    {...rest}
    render={props =>
      isAuthenticated() ? (
        <Component {...props} />
      ) : (
        <Redirect to={{ pathname: '/', state: { from: props.location } }} />
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
                    <PrivateRoute path="/dashboard" component={DashboardPage} />
                    <Redirect to="/" />
                </Switch>
            </div>
        </Router>
    );
};

export default App;