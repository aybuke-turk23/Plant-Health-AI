from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

from src.backend.api_service import analyze_plant_health, get_gemini_chat

app = Flask(__name__, static_folder='src/frontend')
CORS(app)

# --- STATIC FILES ------------------------------------------------------------

@app.route('/')
def index():
    """Serves the main index.html from the frontend static folder."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    """Serves static assets such as CSS, JS, and images."""
    return send_from_directory(app.static_folder, path)

# --- ANALYSIS ENDPOINT -------------------------------------------------------

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Receives an image, runs plant health analysis, and returns results."""
    if 'file' not in request.files:
        return jsonify({"detail": "No image file selected for analysis."}), 400

    image = request.files['file']

    # Create uploads directory if it doesn't exist
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    image_path = os.path.join("uploads", image.filename)
    image.save(image_path)

    try:
        result = analyze_plant_health(image_path)

        # Return error if analysis failed
        if "error" in result:
            return jsonify({"detail": result["error"]}), 400

        return jsonify({
            "health_percentage": int(result.get('accuracy', 0)),
            "summary": f"Plant Condition: {result.get('disease', 'Analysis Complete')}",
            "issues":  [f"Detection: {result.get('status', 'sick')}"],
            "recommendations": [result.get('treatment') or "Isolate the plant and monitor humidity levels."],
            # Raw fields used by the frontend chatbot context
            "disease":   result.get('disease', ''),
            "status":    result.get('status', ''),
            "accuracy":  int(result.get('accuracy', 0)),
            "treatment": result.get('treatment', ''),
        })

    except Exception as e:
        return jsonify({"detail": f"Analysis engine error: {str(e)}"}), 500

# --- CHAT ENDPOINT -----------------------------------------------------------

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handles follow-up questions from the AI assistant panel."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request format."}), 400

    user_message    = data.get('message', '').strip()
    disease_context = data.get('context', '')
    history         = data.get('history', [])

    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    try:
        reply = get_gemini_chat(user_message, disease_context, history)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": f"Chat error: {str(e)}"}), 500

# --- SERVER ENTRY POINT ------------------------------------------------------

if __name__ == '__main__':
    print("Plant Health Analysis System Initializing...")
    app.run(debug=True, port=5000)