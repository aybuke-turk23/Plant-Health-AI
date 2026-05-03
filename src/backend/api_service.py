import os
import base64
import requests
from dotenv import load_dotenv

# .env dosyasından anahtarı yüklüyoruz
load_dotenv()
API_KEY = os.getenv("PLANT_ID_API_KEY")

def analyze_plant_health(image_path):
    """
    Seçilen resmi API'ye gönderir ve analiz sonucunu döner.
    """
    if not API_KEY:
        print("Hata: API anahtarı bulunamadı! .env dosyasını kontrol edin.")
        return None

    url = "https://plant.id/api/v3/health_assessment"
    
    # Resmi API'nin istediği base64 formatına çeviriyoruz
    with open(image_path, "rb") as file:
        image_data = base64.b64encode(file.read()).decode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Api-Key": API_KEY
    }

    payload = {
        "images": [image_data],
        "latitude": 38.35, # Malatya koordinatları
        "longitude": 38.33,
        "similar_images": True
    }

    try:
        print(" API'ye istek gönderiliyor...")
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Bağlantı Hatası: {e}")
        return None