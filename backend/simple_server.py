"""
Simple Test Server for Model Optimization Prompt Generator
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask, jsonify
from flask_cors import CORS
from model_optimizer import ModelOptimizationPromptGenerator
from template_library import PromptTemplateLibrary

app = Flask(__name__)
CORS(app)

# Initialize core components
generator = ModelOptimizationPromptGenerator()
template_library = PromptTemplateLibrary()

@app.route('/')
def index():
    return jsonify({
        'message': 'Model Optimization Prompt Generator API',
        'status': 'running',
        'version': '1.0.0'
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'models_count': len(generator.get_supported_models()),
        'templates_count': len(template_library.get_all_categories())
    })

@app.route('/api/models')
def get_models():
    models = generator.get_supported_models()
    model_info = {}
    
    for model in models:
        model_info[model] = generator.get_model_info(model)
    
    return jsonify({
        'success': True,
        'models': models,
        'model_details': model_info,
        'total_count': len(models)
    })

@app.route('/api/test')
def test_optimization():
    """Quick test endpoint"""
    test_task = "Write a Python function to read CSV files"
    result = generator.generate_optimized_prompt(test_task, 'gpt-4')
    
    return jsonify({
        'success': True,
        'test_task': test_task,
        'result': result
    })

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Simple Test Server Starting...")
    print(f"📍 Models: {generator.get_supported_models()}")
    print(f"📍 Templates: {template_library.get_all_categories()}")
    print("📍 Server: http://localhost:5000")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True) 