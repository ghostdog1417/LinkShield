import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ScatterChart, Scatter } from 'recharts';
import apiClient from '../services/apiClient';
import './EDA.css';

function EDA() {
  const [edaData, setEdaData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEdaData();
  }, []);

  const fetchEdaData = async () => {
    try {
      const response = await apiClient.get('/eda');
      setEdaData(response.data);
    } catch (error) {
      console.error('Failed to fetch EDA data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="eda-loading">Loading analytics...</div>;
  }

  return (
    <div className="eda-container">
      <div className="eda-header">
        <h1>Exploratory Data Analysis</h1>
        <p>Deep dive into feature distributions and patterns</p>
      </div>

      {edaData && (
        <div className="eda-grid">
          <div className="eda-card">
            <h2>Feature Importance</h2>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={edaData.feature_importance || []}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="feature" stroke="var(--text-secondary)" angle={-45} textAnchor="end" height={100} />
                <YAxis stroke="var(--text-secondary)" />
                <Tooltip />
                <Bar dataKey="importance" fill="var(--accent)" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="eda-card">
            <h2>Class Distribution</h2>
            <div className="distribution-bars">
              {edaData.class_distribution && Object.entries(edaData.class_distribution).map(([label, count]) => (
                <div key={label} className="distribution-item">
                  <span>{label}</span>
                  <div className="bar-container">
                    <div
                      className={`bar ${label === 'safe' ? 'safe' : 'suspicious'}`}
                      style={{ width: `${(count / Math.max(...Object.values(edaData.class_distribution))) * 100}%` }}
                    />
                  </div>
                  <span className="count">{count}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="eda-card full-width">
            <h2>URL Length vs Malicious Probability</h2>
            <ResponsiveContainer width="100%" height={300}>
              <ScatterChart>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="url_length" stroke="var(--text-secondary)" name="URL Length" />
                <YAxis stroke="var(--text-secondary)" name="Malicious Score" />
                <Tooltip />
                <Scatter name="URLs" data={edaData.scatter_data || []} fill="var(--accent)" />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
}

export default EDA;
