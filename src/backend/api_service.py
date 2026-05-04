import os
import base64
import requests
import datetime
from dotenv import load_dotenv
from src.backend.security_manager import validate_input, check_rate_limit  # Load API key from .env file

# Security Control: Never hardcode the API key
load_dotenv()
API_KEY = os.getenv("PLANT_ID_API_KEY")

def analyze_plant_health(image_path):
    # 1. Rate Limit Control
    can_request, rate_msg = check_rate_limit()
    if not can_request:
        print(rate_msg)
        return None

    # 2. File Validation Control
    is_valid, val_msg = validate_input(image_path)
    if not is_valid:
        print(val_msg)
        return None
    
    # ... API request logic continues here ...
    """
    1. Security Check (is_plant)
    2. Error Handling (Exception Handling)
    3. Data Parsing (Data Schema)
    """
    if not API_KEY:
        return {"error": "API key not found! Please check the .env file."}

    url = "https://plant.id/api/v3/health_assessment"
    
    try:
        # Convert image to base64 format
        with open(image_path, "rb") as file:
            image_data = base64.b64encode(file.read()).decode("utf-8")

        payload = {
            "images": [image_data],
            "latitude": 38.67,  # Coordinates (example location)
            "longitude": 39.22,
            "similar_images": True
        }

        # API Request (timeout added to prevent connection issues)
        response = requests.post(url, json=payload, headers={"Api-Key": API_KEY}, timeout=20)
        
        # Error Handling: Catch API credit exhaustion (402)
        if response.status_code == 402:
            return {"error": "API credits are exhausted!"}
            
        response.raise_for_status()
        raw_data = response.json()

        # --- Logical Security Check ---
        # Stop process if the image is not a plant
        result_data = raw_data.get("result", {})
        if not result_data.get("is_plant", {}).get("binary", False):
            return {"error": "This is not a plant! Analysis stopped."}

        # --- Logical Data Parsing ---
        # Convert response into clean JSON format for frontend
        disease_info = result_data.get("disease", {}).get("suggestions", [{}])[0]
        
        clean_output = {
            "status": "healthy" if result_data.get("is_healthy", {}).get("binary", False) else "sick",
            "disease": disease_info.get("name", "Unknown"),
            "accuracy": int(disease_info.get("probability", 0) * 100),
            "treatment": disease_info.get("details", {}).get("treatment", "No recommendation found.")
        }

        # Logging for reporting purposes
        with open("analysis_history.log", "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now()}: {clean_output['disease']} - {clean_output['accuracy']}%\n")

        return clean_output

    except requests.exceptions.ConnectionError:
        # Error Handling: Prevent crash if internet connection is lost
        return {"error": "Please check your internet connection."}
    except Exception as e:
        return {"error": f"System error: {str(e)}"}