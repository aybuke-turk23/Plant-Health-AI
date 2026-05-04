from src.backend.api_service import analyze_plant_health

# Path to the test image from your dataset
# Ensure this file exists in the root directory
# Use forward slashes directly, no need for raw string (r"")
TEST_IMAGE_PATH = "data/processed/tomato/fffee500-8469-4c0f-a17d-d95c5516b446___Matt.S_CG 6210.JPG"

# Name of the test image to be used
TEST_IMAGE_PATH = "test_plant.jpg"

def run_api_test():
  
    print(f"--- Manual Test Started: {TEST_IMAGE_PATH} ---")
    
    # Testing the shared logic inside api_service.py
    result = analyze_plant_health(TEST_IMAGE_PATH)

    if "error" in result:
        print(f"❌ ERROR: {result['error']}")
    else:
        print("✅ TEST SUCCESSFUL! Backend data is ready")
        print(f"Result: {result}")


if __name__ == "__main__":
    run_api_test()