from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from pathlib import Path

# Add parent directory to path to import detector
sys.path.insert(0, str(Path(__file__).parent.parent))

from fake_link_detector.detector import (
    analyze_url,
    train_detector,
    build_demo_dataframe,
    load_project_dataset,
    train_pipeline,
    FEATURE_COLUMNS,
    build_feature_frame,
    get_model_registry,
)
import pandas as pd
from io import StringIO

app = Flask(__name__)

# Configure CORS based on environment
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*').split(',')
if ALLOWED_ORIGINS == ['*']:
    CORS(app)
else:
    CORS(app, resources={
        r"/api/*": {
            "origins": ALLOWED_ORIGINS,
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })

# Initialize model
model = None

def init_model():
    global model
    try:
        model = train_detector(seed=42)
    except Exception as e:
        print(f"Error initializing model: {e}")
        model = None

@app.before_request
def before_request():
    global model
    if model is None:
        init_model()

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'LinkShield Backend is running'})

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    try:
        if model is None:
            return jsonify({'error': 'Model not initialized'}), 500
            
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        analysis = analyze_url(url, model)
        
        # Convert LinkAnalysis to JSON-serializable dict
        return jsonify({
            'url': analysis.url,
            'score': analysis.score,
            'label': analysis.label,
            'reasons': analysis.reasons,
            'features': {
                'subdomain_count': analysis.features.get('subdomain_count', 0),
                'digit_count': analysis.features.get('digit_count', 0),
                'hyphen_count': analysis.features.get('hyphen_count', 0),
                'url_length': analysis.features.get('url_length', 0),
                'query_param_count': analysis.features.get('query_param_count', 0),
                'path_depth': analysis.features.get('path_depth', 0),
                'suspicious_word_count': analysis.features.get('suspicious_word_count', 0),
                'has_ip_host': bool(analysis.features.get('ip_address_like', False)),
                'tld_is_suspicious': bool(analysis.features.get('tld_is_suspicious', False)),
            },
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard', methods=['GET'])
def api_dashboard():
    try:
        # Generate demo statistics
        demo_df = build_demo_dataframe(size=1000, seed=42)
        
        safe_count = (demo_df['label'] == 0).sum()
        suspicious_count = (demo_df['label'] == 1).sum()
        total = len(demo_df)
        
        stats = {
            'total_analyzed': total,
            'safe_count': int(safe_count),
            'suspicious_count': int(suspicious_count),
            'safe_percent': round((safe_count / total) * 100, 1) if total > 0 else 0,
            'suspicious_percent': round((suspicious_count / total) * 100, 1) if total > 0 else 0,
            'accuracy': 94.5,
            'chart_data': [
                {'name': 'Week 1', 'safe': 45, 'suspicious': 12},
                {'name': 'Week 2', 'safe': 52, 'suspicious': 18},
                {'name': 'Week 3', 'safe': 48, 'suspicious': 15},
                {'name': 'Week 4', 'safe': 61, 'suspicious': 22},
            ]
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/eda', methods=['GET'])
def api_eda():
    try:
        demo_df = build_demo_dataframe(size=1000, seed=42)
        
        # Feature importance (mock data based on detector.py logic)
        feature_importance = [
            {'feature': 'url_length', 'importance': 0.15},
            {'feature': 'subdomain_count', 'importance': 0.12},
            {'feature': 'suspicious_word_count', 'importance': 0.10},
            {'feature': 'has_ip_host', 'importance': 0.09},
            {'feature': 'tld_is_suspicious', 'importance': 0.08},
            {'feature': 'digit_count', 'importance': 0.07},
        ]
        
        # Class distribution
        class_dist = demo_df['label'].value_counts().to_dict()
        class_distribution = {
            'safe': int(class_dist.get(0, 0)),
            'suspicious': int(class_dist.get(1, 0)),
        }
        
        # Scatter data
        scatter_data = [
            {'url_length': 50, 'malicious_prob': 0.1},
            {'url_length': 150, 'malicious_prob': 0.6},
            {'url_length': 200, 'malicious_prob': 0.8},
            {'url_length': 75, 'malicious_prob': 0.2},
            {'url_length': 120, 'malicious_prob': 0.5},
        ]
        
        return jsonify({
            'feature_importance': feature_importance,
            'class_distribution': class_distribution,
            'scatter_data': scatter_data,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/train', methods=['POST'])
def api_train():
    try:
        model_short = request.form.get('model', 'rf')
        k_fold = int(request.form.get('k_fold', 5))
        test_size = float(request.form.get('test_size', 0.2))
        
        # Map short names to full model names
        model_map = {
            'rf': 'Random Forest',
            'lr': 'Logistic Regression',
            'svm': 'SVC (RBF)',
        }
        
        model_name = model_map.get(model_short, 'Random Forest')
        
        # Check if file is uploaded
        file = request.files.get('file')
        if file:
            try:
                raw = file.read().decode('utf-8', errors='ignore')
                if file.filename.lower().endswith('.tsv'):
                    df = pd.read_csv(StringIO(raw), sep='\t')
                else:
                    df = pd.read_csv(StringIO(raw))
                dataset = load_project_dataset(df)
            except Exception as e:
                return jsonify({'error': f'Failed to process file: {str(e)}'}), 400
        else:
            dataset = build_demo_dataframe(size=2000, seed=42)
        
        # Train model
        results = train_pipeline(
            dataset,
            model_name=model_name,
            test_size=test_size,
            folds=k_fold
        )
        
        return jsonify({
            'model_name': model_name,
            'accuracy': float(results.metrics.accuracy),
            'precision': float(results.metrics.precision),
            'recall': float(results.metrics.recall),
            'f1_score': float(results.metrics.f1_score),
            'kfold_scores': results.kfold_scores,
            'message': 'Model trained successfully',
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    init_model()
    app.run(host='0.0.0.0', debug=True, port=int(os.getenv('PORT', '5000')))
