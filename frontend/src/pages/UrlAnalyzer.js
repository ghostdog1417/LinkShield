import React, { useState, useEffect } from 'react';
import { AlertCircle, CheckCircle, Search } from 'lucide-react';
import apiClient from '../services/apiClient';
import './UrlAnalyzer.css';

function UrlAnalyzer({ setLoading }) {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);

  const analyzeUrl = async (e) => {
    e.preventDefault();
    if (!url.trim()) return;

    setAnalyzing(true);
    setError(null);
    setResult(null);

    try {
      const response = await apiClient.post('/analyze', { url });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Analysis failed. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  };

  const isSafe = result?.label === 'safe';

  return (
    <div className="analyzer-container">
      <div className="analyzer-header">
        <h1>URL Analyzer</h1>
        <p>Check if a URL is safe or potentially malicious</p>
      </div>

      <div className="analyzer-card">
        <form onSubmit={analyzeUrl} className="analyzer-form">
          <div className="input-group">
            <Search size={20} />
            <input
              type="url"
              placeholder="Enter URL (e.g., https://example.com)"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              disabled={analyzing}
            />
            <button type="submit" disabled={analyzing || !url.trim()}>
              {analyzing ? 'Analyzing...' : 'Analyze'}
            </button>
          </div>
        </form>

        {error && (
          <div className="error-message">
            <AlertCircle size={20} />
            {error}
          </div>
        )}

        {result && (
          <div className={`result ${isSafe ? 'safe' : 'suspicious'}`}>
            <div className="result-header">
              {isSafe ? (
                <CheckCircle size={32} className="icon-success" />
              ) : (
                <AlertCircle size={32} className="icon-danger" />
              )}
              <div>
                <h2>{isSafe ? 'Safe Link' : 'Suspicious Link'}</h2>
                <p>Risk Score: {(result.score * 100).toFixed(1)}%</p>
              </div>
            </div>

            {result.reasons && result.reasons.length > 0 && (
              <div className="reasons">
                <h3>Detection Reasons:</h3>
                <ul>
                  {result.reasons.map((reason, idx) => (
                    <li key={idx}>{reason}</li>
                  ))}
                </ul>
              </div>
            )}

            {result.features && (
              <div className="features">
                <h3>URL Features</h3>
                <div className="feature-grid">
                  {Object.entries(result.features).map(([key, value]) => (
                    <div key={key} className="feature-item">
                      <span className="feature-name">{key}</span>
                      <span className="feature-value">{String(value)}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default UrlAnalyzer;
