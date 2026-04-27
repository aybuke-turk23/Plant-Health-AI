import sqlite3
import os
from datetime import datetime

# 1. Veri Klasörü ve Otomatik Klasör Oluşturma [cite: 97, 98]
DB_PATH = 'database/plant_health.sqlite'

def veritabani_hazirla():
    # Klasör yoksa hata vermemesi için otomatik oluşturma ekliyoruz [cite: 99, 100]
    if not os.path.exists('database'):
        os.makedirs('database')
        print("database/ klasörü başarıyla oluşturuldu.")

    baglanti = None
    try:
        # Teknolojinin Seçilmesi: SQLite [cite: 62]
        baglanti = sqlite3.connect(DB_PATH)
        cursor = baglanti.cursor()

        # 2. Analiz Tablosuna "Bitki Türü" (plant_type) Ekleme [cite: 101, 105]
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plant_type TEXT NOT NULL,
                image_path TEXT NOT NULL,
                result TEXT NOT NULL,
                confidence REAL NOT NULL,
                date TEXT NOT NULL
            )
        ''')

        # Plants (Bitkiler) Tablosu [cite: 67]
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Plants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                health_status TEXT NOT NULL
            )
        ''')

        # Remedies (Çözüm Önerileri) Tablosu [cite: 69]
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Remedies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disease_name TEXT NOT NULL,
                treatment TEXT NOT NULL
            )
        ''')

        baglanti.commit()
        print("Veritabanı yapısı ve tablolar başarıyla hazırlandı.")
    except sqlite3.Error as e:
        # 3. Exception Handling (Hata Yönetimi) [cite: 107, 109, 110]
        print(f"Veritabanı hatası kanka: {e}")
    finally:
        if baglanti:
            baglanti.close()

# 1. Kayıt: Analiz sonucunu veritabanına ekleme (Revize edildi) [cite: 72, 106]
def analiz_kaydet(plant_type, image_path, result, confidence):
    baglanti = None
    try:
        baglanti = sqlite3.connect(DB_PATH)
        cursor = baglanti.cursor()
        
        # Tarih formatı ilerideki grafikler için düzgün tutulmalıdır [cite: 76]
        tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Sorguda plant_type da yer almalı [cite: 106]
        cursor.execute('''
            INSERT INTO Analyses (plant_type, image_path, result, confidence, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (plant_type, image_path, result, confidence, tarih))
        
        baglanti.commit()
        print(f"Analiz kaydedildi: {plant_type} - {result}")
    except sqlite3.Error as e:
        print(f"Kayıt sırasında hata oluştu: {e}")
    finally:
        if baglanti:
            baglanti.close()

# 2. Listeleme: Geçmişteki tüm analizleri tarih sırasına göre getirme [cite: 73]
def analizleri_listele():
    baglanti = None
    try:
        baglanti = sqlite3.connect(DB_PATH)
        cursor = baglanti.cursor()
        cursor.execute('SELECT * FROM Analyses ORDER BY date DESC')
        veriler = cursor.fetchall()
        return veriler
    except sqlite3.Error as e:
        print(f"Listeleme hatası: {e}")
        return []
    finally:
        if baglanti:
            baglanti.close()

# 3. Sorgulama: Sadece belirli bir hastalığa sahip bitkileri filtreleme [cite: 74]
def hastalikli_bitkileri_getir(hastalik_adi):
    baglanti = None
    try:
        baglanti = sqlite3.connect(DB_PATH)
        cursor = baglanti.cursor()
        cursor.execute('SELECT * FROM Analyses WHERE result = ?', (hastalik_adi,))
        veriler = cursor.fetchall()
        return veriler
    except sqlite3.Error as e:
        print(f"Sorgulama hatası: {e}")
        return []
    finally:
        if baglanti:
            baglanti.close()

if __name__ == "__main__":
    # Veritabanı dosyasını ve klasörünü oluşturur [cite: 112]
    veritabani_hazirla()
    
    # Yeni yapıya uygun test kaydı (Domates, Patates veya Biber için) [cite: 103, 113]
    print("\n--- Sistem Test Ediliyor ---")
    analiz_kaydet("Domates", "data/raw/tomato/sample.jpg", "Bakteriyel Leke", 0.98)
    
    print("\nVeritabanı sistemi sağlam ve kullanıma hazır. [cite: 114]")