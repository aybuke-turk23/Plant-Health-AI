import os
import base64
import requests
import datetime
from google import genai
from dotenv import load_dotenv
from src.backend.security_manager import validate_input, check_rate_limit

# Load API keys from .env file
load_dotenv()
API_KEY    = os.getenv("PLANT_ID_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_KEY) if GEMINI_KEY else None
GEMINI_MODEL = "gemini-2.5-flash"

# --- SINGLE-TURN ADVICE (called after analysis) ------------------------------

def get_gemini_advice(plant_status, disease_name):
    """Fetches a short expert recommendation from Gemini based on analysis result."""
    if not client:
        return "Gemini API key not found. Please check your .env file."

    if plant_status == "healthy":
        prompt = (
            f"A plant analysis was performed and the plant is healthy. "
            f"Plant type: {disease_name}. "
            f"Give a short, 2-sentence tip on how to keep this plant healthy."
        )
    else:
        prompt = (
            f"A plant analysis was performed and '{disease_name}' was detected. "
            f"Suggest 3 simple emergency treatment steps for this disease. "
            f"Keep the response short and concise."
        )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Gemini Error: {str(e)}")
        return "AI recommendations are currently unavailable."

# --- MULTI-TURN CHAT (called by /api/chat endpoint) -------------------------

def get_gemini_chat(user_message, disease_context, history):
    """
    Sends a request to Gemini for multi-turn conversation.
    - disease_context : context string from the analysis result
    - history         : [{"role": "user"|"model", "content": "..."}, ...]
    """
    if not client:
        return "Gemini API key not found. Please check your .env file."

    system_instruction = (
        "You are an expert agricultural assistant for the Plant-Health-AI project. "
        "You only provide technical and helpful information about plant diseases, "
        "care, and treatment. Politely decline to answer questions outside this scope."
    )

    # Convert chat history to Gemini format
    gemini_history = []
    for msg in history:
        role = msg.get("role", "user")
        gemini_history.append(
            genai.types.Content(
                role=role,
                parts=[genai.types.Part(text=msg.get("content", ""))]
            )
        )

    # Prepend disease context to the first message if no history exists yet
    if disease_context and not gemini_history:
        first_msg = (
            f"Analysis context: {disease_context}\n\n"
            f"User question: {user_message}"
        )
    else:
        first_msg = user_message

    try:
        chat_session = client.chats.create(
            model=GEMINI_MODEL,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction
            ),
            history=gemini_history
        )
        response = chat_session.send_message(first_msg)
        return response.text
    except Exception as e:
        print(f"Gemini Chat Error: {str(e)}")
        return "The AI is currently unable to respond. Please try again."

# --- MAIN ANALYSIS FUNCTION -------------------------------------------------

def analyze_plant_health(image_path):
    # 1. Rate limit check
    can_request, rate_msg = check_rate_limit()
    if not can_request:
        return {"error": rate_msg}

    # 2. File validation
    is_valid, val_msg = validate_input(image_path)
    if not is_valid:
        return {"error": val_msg}

    if not API_KEY:
        return {"error": "Plant.id API key not found! Please check your .env file."}

    url = "https://plant.id/api/v3/health_assessment"

    try:
        # Encode image to base64
        with open(image_path, "rb") as file:
            image_data = base64.b64encode(file.read()).decode("utf-8")

        payload = {
            "images": [image_data],
            "latitude": 38.67,
            "longitude": 39.22,
            "similar_images": True
        }

        # Send request to Plant.id API
        response = requests.post(
            url,
            json=payload,
            headers={"Api-Key": API_KEY},
            timeout=20
        )

        if response.status_code == 402:
            return {"error": "Plant.id API credit exhausted!"}

        response.raise_for_status()
        raw_data = response.json()

        result_data = raw_data.get("result", {})

        # Safety check: stop if the image is not a plant
        if not result_data.get("is_plant", {}).get("binary", False):
            return {"error": "This is not a plant! Please upload a plant photo."}

        # Parse response data
        disease_info = result_data.get("disease", {}).get("suggestions", [{}])[0]
        status       = "healthy" if result_data.get("is_healthy", {}).get("binary", False) else "sick"
        disease      = disease_info.get("name", "Unknown")
        accuracy     = int(disease_info.get("probability", 0) * 100)

        # Fetch AI treatment recommendation from Gemini
        ai_recommendation = get_gemini_advice(status, disease)

        # Log the analysis result
        with open("analysis_history.log", "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now()}: {disease} - %{accuracy}\n")

        return {
            "status":    status,
            "disease":   disease,
            "accuracy":  accuracy,
            "treatment": ai_recommendation
        }

    except requests.exceptions.ConnectionError:
        return {"error": "Please check your internet connection."}
    except requests.exceptions.Timeout:
        return {"error": "Plant.id API did not respond. Please try again."}
    except Exception as e:
        print(f"System Error: {str(e)}")
        return {"error": f"System error: {str(e)}"}