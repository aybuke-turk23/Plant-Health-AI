import sqlite3
from datetime import datetime

# 1. Teknolojinin Seçilmesi: SQLite [cite: 62]
def veritabani_hazirla():
    # database/plant_health.sqlite yapısını oluşturur [cite: 35]
    baglanti = sqlite3.connect('plant_health.sqlite')
    cursor = baglanti.cursor()

    # 2. Tablo Yapısının Tasarlanması [cite: 64]
    
    # Plants (Bitkiler) Tablosu [cite: 67]
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            health_status TEXT NOT NULL
        )
    ''')

    # Analyses (Analizler) Tablosu [cite: 68]
    # Not: Tarih formatı ilerideki grafikler için düzgün tutulmalıdır [cite: 76]
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT NOT NULL,
            result TEXT NOT NULL,
            confidence REAL NOT NULL,
            date TEXT NOT NULL
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
    baglanti.close()
    print("Veritabanı ve tablolar başarıyla oluşturuldu!")
# 1. Kayıt: Analiz sonucunu veritabanına ekleme [cite: 72]
def analiz_kaydet(image_path, result, confidence):
    baglanti = sqlite3.connect('plant_health.sqlite')
    cursor = baglanti.cursor()
    
    # Tarih formatını düzgün tutmak için 
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO Analyses (image_path, result, confidence, date)
        VALUES (?, ?, ?, ?)
    ''', (image_path, result, confidence, tarih))
    
    baglanti.commit()
    baglanti.close()
    print(f"Analiz kaydedildi: {result}")

# 2. Listeleme: Geçmişteki tüm analizleri tarih sırasına göre getirme [cite: 73]
def analizleri_listele():
    baglanti = sqlite3.connect('plant_health.sqlite')
    cursor = baglanti.cursor()
    
    cursor.execute('SELECT * FROM Analyses ORDER BY date DESC')
    veriler = cursor.fetchall()
    
    baglanti.close()
    return veriler

# 3. Sorgulama: Sadece belirli bir hastalığa sahip bitkileri filtreleme [cite: 74]
def hastalikli_bitkileri_getir(hastalik_adi):
    baglanti = sqlite3.connect('plant_health.sqlite')
    cursor = baglanti.cursor()
    
    cursor.execute('SELECT * FROM Analyses WHERE result = ?', (hastalik_adi,))
    veriler = cursor.fetchall()
    
    baglanti.close()
    return veriler

if __name__ == "__main__":
    # Bu kısım sadece sen bu dosyayı doğrudan çalıştırdığında (python database_manager.py) devreye girer.
    # Diğer arkadaşlar bu dosyayı kendi kodlarına eklediklerinde burası çalışmaz.
    
    veritabani_hazirla()
    print("Veritabanı sistemi aktif ve kullanıma hazır.")