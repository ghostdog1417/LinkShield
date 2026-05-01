import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';
import apiClient from '../services/apiClient';
import './Dashboard.css';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await apiClient.get('/dashboard');
      setStats(response.data);
      setChartData(response.data.chart_data || []);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="dashboard-loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <p>Real-time URL Detection Statistics</p>
      </div>

      {stats && (
        <>
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total URLs Analyzed</h3>
              <div className="stat-value">{stats.total_analyzed || 0}</div>
              <p>All time</p>
            </div>
            <div className="stat-card">
              <h3>Safe Links</h3>
              <div className="stat-value safe">{stats.safe_count || 0}</div>
              <p>{stats.safe_percent || 0}% of total</p>
            </div>
            <div className="stat-card">
              <h3>Suspicious Links</h3>
              <div className="stat-value danger">{stats.suspicious_count || 0}</div>
              <p>{stats.suspicious_percent || 0}% of total</p>
            </div>
            <div className="stat-card">
              <h3>Model Accuracy</h3>
              <div className="stat-value">{stats.accuracy || 0}%</div>
              <p>Last trained</p>
            </div>
          </div>

          {chartData.length > 0 && (
            <div className="charts-grid">
              <div className="chart-container">
                <h2>Analysis Distribution</h2>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                    <XAxis dataKey="name" stroke="var(--text-secondary)" />
                    <YAxis stroke="var(--text-secondary)" />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="safe" fill="#10b981" />
                    <Bar dataKey="suspicious" fill="#ef4444" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default Dashboard;
