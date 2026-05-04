from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

# Import the core analysis logic from the backend service
from src.backend.api_service import analyze_plant_health 

app = Flask(__name__, static_folder='src/frontend')
CORS(app) # Enable CORS for frontend-backend communication

# --- ROUTE DEFINITIONS ---

@app.route('/')
def index():
    """Serves the main index.html file from the frontend static folder."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    """Serves static assets such as CSS, JS, and images."""
    return send_from_directory(app.static_folder, path)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Bridge endpoint that handles analysis requests from the frontend.
    """
    # 1. File Validation: Checking if the 'file' key exists in the request
    if 'file' not in request.files:
        return jsonify({"detail": "No image file selected for analysis."}), 400
    
    image = request.files['file']
    
    # 2. Storage Directory Check
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    
    # 3. Save the uploaded image
    image_path = os.path.join("uploads", image.filename)
    image.save(image_path)
    
    try:
        # 4. Backend Analysis: Execute the logic within api_service
        result = analyze_plant_health(image_path)
        
        # 5. Data Transformation: Map backend results to frontend requirements
        # Frontend expects health_percentage, issues, and recommendations (list).
        return jsonify({
            "health_percentage": int(result.get('accuracy', 0)),
            "summary": f"Plant Condition: {result.get('disease', 'Analysis Successful')}",
            "issues": [f"Detection: {result.get('status', 'sick')}"],
            # Provide a fallback recommendation if no specific treatment is found
            "recommendations": [result.get('treatment') or "Isolate the plant and monitor humidity levels."]
        })
        
    except Exception as e:
        # Generic error handling for the analysis engine
        return jsonify({"detail": f"Analysis engine error: {str(e)}"}), 500

if __name__ == '__main__':
    # Initialize the Flask server on port 5000 as expected by the frontend
    print("Siberay Plant Health Analysis System Initializing...")
    app.run(debug=True, port=5000)