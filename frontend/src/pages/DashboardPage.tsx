import React, { useState } from 'react';
import { Switch, Route, useRouteMatch, useHistory } from 'react-router-dom';
import { isAuthenticated } from '../services/auth';
import Sidebar from '../components/Sidebar';
import Recommendations from '../components/Recommendations';
import Notifications from '../components/Notifications';
import Weather from '../components/Weather';
import History from '../components/History';

const DashboardPage: React.FC = () => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const { path } = useRouteMatch();
    const history = useHistory();

    
    React.useEffect(() => {
        if (!isAuthenticated()) {
            history.push('/');
        }
    }, [history]);

    const toggleSidebar = () => {
        setIsSidebarOpen(!isSidebarOpen);
    };

    return (
        <div className="dashboard">
            <Sidebar isOpen={isSidebarOpen} toggleSidebar={toggleSidebar} />
            
            <div className={`main-content ${isSidebarOpen ? 'sidebar-open' : ''}`}>
                <header className="header">
                    <button className="menu-button" onClick={toggleSidebar}>
                        ☰
                    </button>
                    <img src="/agrosmart-logo.svg" alt="AgroSmart" className="logo" height="200"/>
                </header>
                
                <Switch>
                    <Route path={`${path}/recommendations`}>
                        <Recommendations />
                    </Route>
                    <Route path={`${path}/alerts`}>
                        <Notifications />
                    </Route>
                    <Route path={`${path}/history`}>
                        <History />
                    </Route>
                    <Route path={`${path}/weather`}>
                        <Weather />
                    </Route>
                    <Route path={path} exact>
                        <Weather />
                    </Route>
                </Switch>
            </div>
        </div>
    );
};

export default DashboardPage;