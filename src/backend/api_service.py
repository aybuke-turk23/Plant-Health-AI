import os
import base64
import requests
import datetime
from dotenv import load_dotenv
from src.backend.security_manager import validate_input, check_rate_limit# .env dosyasından anahtarı yüklüyoruz

# Gizlilik Kontrolü: API anahtarını asla elle yazmıyoruz
load_dotenv()
API_KEY = os.getenv("PLANT_ID_API_KEY")

def analyze_plant_health(image_path):
    # 1. Bekleme Süresi Kontrolü
    can_request, rate_msg = check_rate_limit()
    if not can_request:
        print(rate_msg)
        return None

    # 2. Dosya Geçerlilik Kontrolü
    is_valid, val_msg = validate_input(image_path)
    if not is_valid:
        print(val_msg)
        return None
    
    # ... API çağırma kodları buradan devam eder ...
    """
   
    1. Güvenlik Kontrolü (is_plant)
    2. Hata Yönetimi (Exception Handling)
    3. Veri Ayrıştırma (Data Schema)
    """
    if not API_KEY:
        return {"error": "API anahtarı bulunamadı! .env dosyasını kontrol edin."}

    url = "https://plant.id/api/v3/health_assessment"
    
    try:
        # Resmi base64 formatına çeviriyoruz
        with open(image_path, "rb") as file:
            image_data = base64.b64encode(file.read()).decode("utf-8")

        payload = {
            "images": [image_data],
            "latitude": 38.67, # Elazığ koordinatları
            "longitude": 39.22,
            "similar_images": True
        }

        # API İsteği (Bağlantı kopmalarına karşı timeout eklendi)
        response = requests.post(url, json=payload, headers={"Api-Key": API_KEY}, timeout=20)
        
        # Hata Yakalama: Kredi bittiyse (402) yakalıyoruz
        if response.status_code == 402:
            return {"error": "API kredisi bitti!"}
            
        response.raise_for_status()
        raw_data = response.json()

        # --- MANTIKLI KOD TAŞIMA: Siber Güvenlik ---
        # Eğer gönderilen resim bitki değilse süreci durduruyoruz
        result_data = raw_data.get("result", {})
        if not result_data.get("is_plant", {}).get("binary", False):
            return {"error": "Bu bir bitki değil! Analiz durduruldu."}

        # --- MANTIKLI KOD TAŞIMA: Veri Ayrıştırma (Data Parsing) ---
        # Frontend için istediği o sade JSON formatına çeviriyoruz
        disease_info = result_data.get("disease", {}).get("suggestions", [{}])[0]
        
        clean_output = {
            "status": "healthy" if result_data.get("is_healthy", {}).get("binary", False) else "sick",
            "disease": disease_info.get("name", "Bilinmiyor"),
            "accuracy": int(disease_info.get("probability", 0) * 100),
            "treatment": disease_info.get("details", {}).get("treatment", "Öneri bulunamadı.")
        }

        #  raporlama kaydı tutuluyor
        with open("analysis_history.log", "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now()}: {clean_output['disease']} - %{clean_output['accuracy']}\n")

        return clean_output

    except requests.exceptions.ConnectionError:
        # Hata Yakalama: İnternet koptuğunda crash olmayı engelliyoruz
        return {"error": "İnternet bağlantınızı kontrol edin."}
    except Exception as e:
        return {"error": f"Sistem hatası: {str(e)}"}