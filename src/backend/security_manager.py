import os
import time

# Son istek zamanını takip etmek için (Rate Limiting)
last_request_time = 0

def validate_input(image_path):
    """
    Giriş Doğrulama: Dosya tipi ve boyut kontrolü yapar.
    """
    # 1. Dosya Tipi Kontrolü
    allowed_extensions = ['.jpg', '.jpeg', '.png']
    extension = os.path.splitext(image_path)[1].lower()
    
    if extension not in allowed_extensions:
        return False, f"Hata: {extension} uzantısı kabul edilmez. Sadece JPG ve PNG!"

    # 2. Boyut Sınırı (Maksimum 5MB)
    try:
        file_size = os.path.getsize(image_path) / (1024 * 1024) # MB'a çevir
        if file_size > 5:
            return False, f"Hata: Dosya çok büyük ({file_size:.2f}MB). Sınır 5MB!"
    except FileNotFoundError:
        return False, "Hata: Dosya bulunamadı!"
        
    return True, "Geçerli"

def check_rate_limit():
    """
    Rate Limiting: İki istek arasında 10 saniye bekleme zorunluluğu getirir.
    """
    global last_request_time
    current_time = time.time()
    cooldown = 10 # saniye
    
    if current_time - last_request_time < cooldown:
        remaining = int(cooldown - (current_time - last_request_time))
        return False, f"Hata: Çok hızlı deniyorsunuz! Lütfen {remaining} saniye bekleyin."
    
    last_request_time = current_time
    return True, "İstek gönderilebilir"
