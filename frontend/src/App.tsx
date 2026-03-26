import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { api } from './lib/api';
import Navigation from './components/Navigation';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Prediction from './pages/Prediction';
import Portfolio from './pages/Portfolio';
import Settings from './pages/Settings';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userName, setUserName] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    if (api.isAuthenticated()) {
      setIsAuthenticated(true);
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const decoded: any = JSON.parse(atob(token.split('.')[1]));
          setUserName(decoded.sub || 'User');
        } catch {
          setUserName('User');
        }
      }
    }
    setLoading(false);
  }, []);

  const handleLogout = () => {
    api.logout();
    setIsAuthenticated(false);
    setUserName('');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gradient-to-br from-slate-900 to-slate-800">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
        {isAuthenticated && <Navigation userName={userName} onLogout={handleLogout} />}

        <Routes>
          {!isAuthenticated ? (
            <>
              <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} setUserName={setUserName} />} />
              <Route path="/register" element={<Register />} />
              <Route path="*" element={<Navigate to="/login" replace />} />
            </>
          ) : (
            <>
              <Route path="/" element={<Dashboard />} />
              <Route path="/predict" element={<Prediction />} />
              <Route path="/portfolio" element={<Portfolio />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </>
          )}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
