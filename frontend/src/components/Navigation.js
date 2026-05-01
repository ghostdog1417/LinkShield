import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Shield, BarChart3, Brain, TrendingUp } from 'lucide-react';
import './Navigation.css';

function Navigation() {
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="sidebar">
      <div className="logo">
        <Shield size={32} />
        <span>LinkShield</span>
      </div>

      <ul className="nav-links">
        <li>
          <Link to="/" className={isActive('/') ? 'active' : ''}>
            <BarChart3 size={20} />
            Dashboard
          </Link>
        </li>
        <li>
          <Link to="/analyzer" className={isActive('/analyzer') ? 'active' : ''}>
            <Shield size={20} />
            URL Analyzer
          </Link>
        </li>
        <li>
          <Link to="/eda" className={isActive('/eda') ? 'active' : ''}>
            <TrendingUp size={20} />
            Analytics
          </Link>
        </li>
        <li>
          <Link to="/training" className={isActive('/training') ? 'active' : ''}>
            <Brain size={20} />
            Model Training
          </Link>
        </li>
      </ul>

      <div className="nav-footer">
        <p>LinkShield v1.0</p>
        <p>ML-powered Link Detection</p>
      </div>
    </nav>
  );
}

export default Navigation;
