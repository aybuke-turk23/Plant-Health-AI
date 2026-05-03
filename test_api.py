from src.backend.api_service import analyze_plant_health

# Test edilecek resmin adı
TEST_IMAGE_PATH = "test_plant.jpg"

def run_api_test():
  
    print(f"--- Manuel Test Başlatılıyor: {TEST_IMAGE_PATH} ---")
    
    # api_service.py içindeki paylaştırılmış mantığı test ediyoruz
    result = analyze_plant_health(TEST_IMAGE_PATH)

    if "error" in result:
        print(f"❌ HATA: {result['error']}")
    else:
        print("✅ TEST BAŞARILI! Backend verisi hazır")
        print(f"Sonuç: {result}")

if __name__ == "__main__":
    run_api_test()