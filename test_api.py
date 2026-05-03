from src.backend.api_service import analyze_plant_health

# Path to the test image from your dataset
# Ensure this file exists in the root directory
# Başına 'r' koymaya gerek kalmadan, sadece düz eğik çizgi kullanıyoruz
TEST_IMAGE_PATH = "data/processed/tomato/fffee500-8469-4c0f-a17d-d95c5516b446___Matt.S_CG 6210.JPG"
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
   