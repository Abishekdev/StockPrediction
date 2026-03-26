import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { BarChart3, TrendingUp, Briefcase, Settings, LogOut, Menu, X } from 'lucide-react';
import { useState } from 'react';

interface NavigationProps {
  userName: string;
  onLogout: () => void;
}

const Navigation: React.FC<NavigationProps> = ({ userName, onLogout }) => {
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(false);

  const navItems = [
    { path: '/', label: 'Dashboard', icon: BarChart3 },
    { path: '/predict', label: 'Predictions', icon: TrendingUp },
    { path: '/portfolio', label: 'Portfolio', icon: Briefcase },
    { path: '/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <nav className="glass sticky top-0 z-50 border-b border-blue-500/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 group">
            <BarChart3 className="w-8 h-8 text-blue-400 group-hover:text-blue-300 transition" />
            <span className="text-xl font-bold text-white hidden sm:inline">Stock Predictor</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-1 px-3 py-2 rounded-lg transition ${
                    isActive
                      ? 'bg-blue-500/30 text-blue-300 border border-blue-400/50'
                      : 'text-gray-300 hover:bg-white/5'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </div>

          {/* Right side */}
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-300 hidden sm:inline">Welcome, {userName}</span>
            <button
              onClick={onLogout}
              className="flex items-center space-x-1 px-3 py-2 rounded-lg text-gray-300 hover:bg-red-500/10 hover:text-red-300 transition"
            >
              <LogOut className="w-4 h-4" />
              <span className="hidden sm:inline">Logout</span>
            </button>

            {/* Mobile menu button */}
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="md:hidden text-gray-300 hover:text-white"
            >
              {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden border-t border-blue-500/20 py-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition ${
                    isActive
                      ? 'bg-blue-500/30 text-blue-300'
                      : 'text-gray-300 hover:bg-white/5'
                  }`}
                  onClick={() => setIsOpen(false)}
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navigation;
