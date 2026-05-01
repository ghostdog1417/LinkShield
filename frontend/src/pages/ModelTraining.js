import React, { useState } from 'react';
import { Upload, Brain } from 'lucide-react';
import apiClient from '../services/apiClient';
import './ModelTraining.css';

function ModelTraining({ setLoading }) {
  const [selectedModel, setSelectedModel] = useState('rf');
  const [kfold, setKfold] = useState(5);
  const [testSize, setTestSize] = useState(0.2);
  const [training, setTraining] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);

  const models = [
    { id: 'rf', name: 'Random Forest' },
    { id: 'lr', name: 'Logistic Regression' },
    { id: 'svm', name: 'Support Vector Machine' },
  ];

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setUploadedFile(file);
      setError(null);
    }
  };

  const trainModel = async () => {
    setTraining(true);
    setError(null);
    setResults(null);

    try {
      const formData = new FormData();
      formData.append('model', selectedModel);
      formData.append('k_fold', kfold);
      formData.append('test_size', testSize);
      if (uploadedFile) {
        formData.append('file', uploadedFile);
      }

      const response = await apiClient.post('/train', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setResults(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Training failed. Please try again.');
    } finally {
      setTraining(false);
    }
  };

  return (
    <div className="training-container">
      <div className="training-header">
        <h1>Model Training</h1>
        <p>Train and evaluate fake link detection models</p>
      </div>

      <div className="training-grid">
        <div className="training-config">
          <h2>Configuration</h2>

          <div className="config-group">
            <label>Model</label>
            <select value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)}>
              {models.map((model) => (
                <option key={model.id} value={model.id}>
                  {model.name}
                </option>
              ))}
            </select>
          </div>

          <div className="config-group">
            <label>K-Fold Validation</label>
            <input
              type="number"
              min="2"
              max="10"
              value={kfold}
              onChange={(e) => setKfold(parseInt(e.target.value))}
              disabled={training}
            />
          </div>

          <div className="config-group">
            <label>Test Size</label>
            <input
              type="number"
              min="0.1"
              max="0.5"
              step="0.1"
              value={testSize}
              onChange={(e) => setTestSize(parseFloat(e.target.value))}
              disabled={training}
            />
          </div>

          <div className="config-group">
            <label>Dataset (CSV/TSV)</label>
            <div className="file-input-wrapper">
              <input
                type="file"
                accept=".csv,.tsv"
                onChange={handleFileUpload}
                disabled={training}
              />
              <span>{uploadedFile ? uploadedFile.name : 'No file selected'}</span>
            </div>
          </div>

          <button
            className="train-button"
            onClick={trainModel}
            disabled={training}
          >
            <Brain size={20} />
            {training ? 'Training...' : 'Train Model'}
          </button>
        </div>

        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}

        {results && (
          <div className="results-panel">
            <h2>Training Results</h2>
            <div className="metrics-grid">
              <div className="metric">
                <span className="metric-label">Accuracy</span>
                <span className="metric-value">{(results.accuracy * 100).toFixed(2)}%</span>
              </div>
              <div className="metric">
                <span className="metric-label">Precision</span>
                <span className="metric-value">{(results.precision * 100).toFixed(2)}%</span>
              </div>
              <div className="metric">
                <span className="metric-label">Recall</span>
                <span className="metric-value">{(results.recall * 100).toFixed(2)}%</span>
              </div>
              <div className="metric">
                <span className="metric-label">F1 Score</span>
                <span className="metric-value">{(results.f1_score * 100).toFixed(2)}%</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ModelTraining;
