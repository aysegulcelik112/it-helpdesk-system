/**
 * Ana Uygulama Bileşeni
 */

import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { isAuthenticated, isITStaff, getUser } from './utils/auth';

// Pages
import LoginPage from './pages/LoginPage';
import EmployeeDashboard from './pages/EmployeeDashboard';
import ITDashboard from './pages/ITDashboard';
import TicketDetail from './pages/TicketDetail';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (isAuthenticated()) {
      setUser(getUser());
    }
  }, []);

  // Private Route wrapper
  const PrivateRoute = ({ children }) => {
    return isAuthenticated() ? children : <Navigate to="/" />;
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={
          isAuthenticated() 
            ? <Navigate to={isITStaff() ? "/it-dashboard" : "/dashboard"} />
            : <LoginPage onLogin={setUser} />
        } />
        
        <Route path="/dashboard" element={
          <PrivateRoute>
            <EmployeeDashboard />
          </PrivateRoute>
        } />
        
        <Route path="/it-dashboard" element={
          <PrivateRoute>
            {isITStaff() ? <ITDashboard /> : <Navigate to="/dashboard" />}
          </PrivateRoute>
        } />
        
        <Route path="/ticket/:id" element={
          <PrivateRoute>
            <TicketDetail />
          </PrivateRoute>
        } />
      </Routes>
    </Router>
  );
}

export default App;
