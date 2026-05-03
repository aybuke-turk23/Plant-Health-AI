import json
from src.backend.api_service import analyze_plant_health

# Path to the test image from your dataset
# Ensure this file exists in the root directory
TEST_IMAGE_PATH = "test_plant.jpg"

def run_api_test():
    """
    Executes a health assessment test using the Plant.id API
    and displays the formatted results.
    """
    print(f"--- Analyzing: {TEST_IMAGE_PATH} ---")
    
    # Trigger the API service
    api_response = analyze_plant_health(TEST_IMAGE_PATH)

    if api_response:
        # Display the full raw JSON for debugging purposes
        print("\n[DEBUG] Raw API Response:")
        print(json.dumps(api_response, indent=4, ensure_ascii=False))
        
        # Extract disease suggestions from the response
        results_data = api_response.get("result", {})
        disease_data = results_data.get("disease", {})
        suggestions = disease_data.get("suggestions", [])

        if suggestions:
            # Parse the top result (highest probability)
            top_prediction = suggestions[0]
            disease_name = top_prediction.get("name")
            confidence_score = top_prediction.get("probability", 0)

            print("\n" + "="*30)
            print(f"🚀 API Prediction: {disease_name}")
            print(f"📊 Confidence Score: {confidence_score * 100:.2f}%")
            print("="*30)
        else:
            # Handle cases where the plant is healthy or unidentified
            is_healthy = results_data.get("is_healthy", {}).get("binary", False)
            if is_healthy:
                print("\n✅ Status: The plant appears to be healthy.")
            else:
                print("\n⚠️ Warning: No specific disease could be identified.")
    else:
        # Error handling for connection or API key issues
        print("\n❌ Error: Failed to receive a response from the API.")
        print("Please check your .env file, API key credits, and internet connection.")

if __name__ == "__main__":
    run_api_test()