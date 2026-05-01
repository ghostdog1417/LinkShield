import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import Dashboard from './pages/Dashboard';
import UrlAnalyzer from './pages/UrlAnalyzer';
import ModelTraining from './pages/ModelTraining';
import EDA from './pages/EDA';
import './App.css';

function App() {
  const [loading, setLoading] = useState(false);

  return (
    <Router>
      <div className="app-container">
        <Navigation />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/analyzer" element={<UrlAnalyzer setLoading={setLoading} />} />
            <Route path="/training" element={<ModelTraining setLoading={setLoading} />} />
            <Route path="/eda" element={<EDA />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
