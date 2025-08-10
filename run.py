#!/usr/bin/env python3
"""
Simple runner script for Potato Disease Detection API
This script runs the Flask app directly without gunicorn
"""

import os
import sys

if __name__ == "__main__":
    # Check if model files exist
    model_path = os.path.join(os.path.dirname(__file__), 'model', 'model_unquant.tflite')
    labels_path = os.path.join(os.path.dirname(__file__), 'model', 'labels.txt')
    
    if not os.path.exists(model_path):
        print(f"❌ Error: Model file not found at {model_path}")
        print("Please ensure the model file exists in the model/ directory")
        sys.exit(1)
    
    if not os.path.exists(labels_path):
        print(f"❌ Error: Labels file not found at {labels_path}")
        print("Please ensure the labels file exists in the model/ directory")
        sys.exit(1)
    
    print("🥔 Starting Potato Disease Detection API...")
    print("📁 Model files verified ✅")
    
    # Import and run the app
    from app import app
    
    port = int(os.environ.get('PORT', 8000))
    print(f"🚀 Starting server on http://localhost:{port}")
    print("🔍 Health check: http://localhost:{port}/health")
    print("📋 API documentation: http://localhost:{port}")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=port)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)
