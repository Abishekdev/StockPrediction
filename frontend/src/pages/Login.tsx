import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { api } from '../lib/api';
import { BarChart3, AlertCircle } from 'lucide-react';

interface LoginProps {
  setIsAuthenticated: (value: boolean) => void;
  setUserName: (value: string) => void;
}

const Login: React.FC<LoginProps> = ({ setIsAuthenticated, setUserName }) => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await api.login(username, password);
      setUserName(response.user.username);
      setIsAuthenticated(true);
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Logo and Title */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <BarChart3 className="w-10 h-10 text-blue-400" />
            <h1 className="text-4xl font-bold text-white">Stock Predictor</h1>
          </div>
          <p className="text-gray-400">AI-Powered Stock Price Prediction</p>
        </div>

        {/* Login Form */}
        <div className="glass rounded-2xl p-8 fade-in">
          <h2 className="text-2xl font-bold text-white mb-6">Login</h2>

          {error && (
            <div className="mb-4 p-3 bg-red-500/10 border border-red-500/50 rounded-lg flex items-start space-x-2">
              <AlertCircle className="w-5 h-5 text-red-400 mt-0.5 flex-shrink-0" />
              <p className="text-sm text-red-300">{error}</p>
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Username
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter your username"
                className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500/50 focus:bg-white/10 transition"
                disabled={loading}
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500/50 focus:bg-white/10 transition"
                disabled={loading}
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2 bg-gradient-to-r from-blue-600 to-blue-400 text-white font-semibold rounded-lg hover:from-blue-500 hover:to-blue-300 disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </form>

          <p className="text-center text-gray-400 text-sm mt-6">
            Don't have an account?{' '}
            <Link to="/register" className="text-blue-400 hover:text-blue-300 font-semibold">
              Register here
            </Link>
          </p>
        </div>

        {/* Disclaimer */}
        <div className="mt-8 p-4 bg-yellow-500/10 border border-yellow-500/30 rounded-lg text-yellow-300 text-sm">
          <p className="font-semibold mb-1">⚠️ Disclaimer</p>
          <p>
            Predictions are for educational purposes only. Stock market predictions carry
            inherent uncertainty. Never use this as your sole basis for investment decisions.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
