import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import sys
import os

# 1. DOSYA YOLLARINI AYARLAMA (Modüllerin bulunması için kritik)
# Python'ın ana dizindeki database_manager'ı görmesini sağlar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from database_manager import veritabani_hazirla, analiz_kaydet, analizleri_listele # database_manager.py src içindeyse direkt import edilir
    from predict import predict_leaf # predict.py src içindeyse direkt import edilir
except ImportError as e:
    print(f"Hata: Modüller yüklenemedi. Lütfen dosya konumlarını kontrol et kanka! \nDetay: {e}")

resim_yolu = ""

# 2. RESİM SEÇME FONKSİYONU
def resim_sec():
    global resim_yolu
    dosya = filedialog.askopenfilename(
        title="Bir Bitki Yaprağı Seç",
        filetypes=[("Resim Dosyaları", "*.jpg *.jpeg *.png")]
    )

    if dosya:
        resim_yolu = dosya
        img = Image.open(dosya)
        img = img.resize((250, 250)) # Arayüz için boyutlandırma
        img = ImageTk.PhotoImage(img)
        
        label_resim.config(image=img)
        label_resim.image = img
        sonuc_label.config(text="Resim hazır, analiz butonuna bas!", fg="#1b5e20")

# 3. ANALİZ VE KAYIT FONKSİYONU (Ana Motor)
def analiz_et():
    if not resim_yolu:
        sonuc_label.config(text="⚠️ Lütfen önce bir resim seç kanka!", fg="red")
        return

    sonuc_label.config(text="🔍 Analiz ediliyor, lütfen bekle...", fg="#1b5e20")
    pencere.update() # Arayüzün donmasını engellemek için

    try:
        # AI Modelini Çalıştır
        hastalik, guven = predict_leaf(resim_yolu)
        
        if hastalik:
            # Ekrana Yazdır
            sonuc_metni = f"🌿 Sonuç: {hastalik}\n🎯 Güven Oranı: %{guven:.2f}"
            sonuc_label.config(text=sonuc_metni, fg="#2e7d32")
            
            # Veritabanına Kaydet
            # Bitki türünü tahmin sonucunun ilk kelimesinden alıyoruz (Örn: Tomato)
            bitki_turu = hastalik.split()[0] 
            analiz_kaydet(bitki_turu, resim_yolu, hastalik, guven)
            print(f"✅ Başarılı: {hastalik} veritabanına işlendi.")
        else:
            sonuc_label.config(text="❌ Tahmin başarısız!", fg="red")

    except Exception as e:
        sonuc_label.config(text=f"Hata: {str(e)}", fg="red")

def gecmisi_goruntule():
    # 1. Yeni bir pencere oluştur
    gecmis_penceresi = tk.Toplevel(pencere)
    gecmis_penceresi.title("Analiz Geçmişi")
    gecmis_penceresi.geometry("700x450")
    gecmis_penceresi.config(bg="#f1f8e9")

    # Başlık
    tk.Label(
        gecmis_penceresi, 
        text="📋 Kayıtlı Analiz Geçmişi", 
        font=("Arial", 14, "bold"), 
        bg="#f1f8e9",
        fg="#2e7d32"
    ).pack(pady=15)

    # 2. Kayıtları Veritabanından Çek
    try:
        from database_manager import analizleri_listele
        kayitlar = analizleri_listele()
    except Exception as e:
        tk.Label(gecmis_penceresi, text=f"Veri çekme hatası: {e}", fg="red").pack()
        return

    # 3. Liste Alanı ve Scrollbar
    frame = tk.Frame(gecmis_penceresi, bg="#f1f8e9")
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    # Yazı tipi olarak sabit genişlikli (Courier) seçtik ki sütunlar düzgün hizalansın
    liste = tk.Listbox(
        frame, 
        font=("Courier New", 10), 
        width=80, 
        yscrollcommand=scrollbar.set,
        bg="white",
        relief="flat",
        borderwidth=5
    )
    liste.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=liste.yview)

    # 4. Tablo Başlıkları
    header = f"{'Bitki':<12} | {'Teşhis':<20} | {'Güven':<10} | {'Tarih'}"
    liste.insert(tk.END, header)
    liste.insert(tk.END, "-" * 75)

    # 5. Verileri Ekle (Hata Kontrollü)
    if not kayitlar:
        liste.insert(tk.END, "Henüz hiç analiz kaydı bulunmuyor.")
    else:
        for satir in kayitlar:
            try:
                # satir içeriği: (id, plant_type, image_path, result, confidence, date)
                
                # Veri tipi dönüşümleri (Hata almamak için her ihtimale karşı)
                bitki = str(satir[1])
                teshis = str(satir[3])
                tarih = str(satir[5])
                
                # Güven değeri bytes gelirse float'a çeviriyoruz
                raw_guven = satir[4]
                try:
                    if isinstance(raw_guven, bytes):
                        guven_float = float(raw_guven.decode('utf-8'))
                    else:
                        guven_float = float(raw_guven)
                    guven_str = f"{guven_float:.2f}"
                except (ValueError, TypeError):
                    guven_str = str(raw_guven)
                 

                # Satırı formatla
                bilgi = f"{bitki:<12} | {teshis:<20} | {guven_str:<10} | {tarih}"
                liste.insert(tk.END, bilgi)
                
            except Exception as err:
                print(f"Satır işleme hatası: {err}")
                continue # Hatalı satırı atla, uygulamayı çökertme

    # Kapat butonu
    tk.Button(gecmis_penceresi, text="Pencereyi Kapat", command=gecmis_penceresi.destroy, bg="#81c784").pack(pady=10)


# 4. GÖRSEL ARAYÜZ (GUI) TASARIMI
pencere = tk.Tk()
pencere.title("Plant Health AI - Fırat University")
pencere.geometry("450x600")
pencere.config(bg="#f1f8e9")

baslik = tk.Label(
    pencere,
    text="🌱 Plant Health AI",
    font=("Helvetica", 22, "bold"),
    bg="#f1f8e9",
    fg="#2e7d32"
)
baslik.pack(pady=20)

btn_sec = tk.Button(
    pencere,
    text="📂 Resim Seç",
    font=("Arial", 11),
    width=20,
    command=resim_sec,
    bg="white"
)
btn_sec.pack(pady=10)

# Resmin önizlemesinin görüneceği beyaz çerçeve
label_resim = tk.Label(pencere, bg="white", width=300, height=250, relief="solid")
label_resim.pack(pady=10)

btn_analiz = tk.Button(
    pencere,
    text="🔍 Analizi Başlat",
    font=("Arial", 12, "bold"),
    width=20,
    bg="#4caf50",
    fg="white",
    command=analiz_et,
    activebackground="#388e3c"
)
btn_analiz.pack(pady=20)

btn_gecmis = tk.Button(
    pencere,
    text="📋 Geçmişi Görüntüle",
    font=("Arial", 11),
    width=20,
    command=gecmisi_goruntule, # yukarıdaki fonksiyonu çağırır
    bg="#81c784",
    fg="white"
)
btn_gecmis.pack(pady=5)

sonuc_label = tk.Label(
    pencere,
    text="Analiz sonuçları burada görünecek",
    font=("Arial", 11, "italic"),
    bg="#f1f8e9",
    fg="#555",
    justify="center"
)
sonuc_label.pack(pady=15)

# 5. PROGRAMI BAŞLATMA
if __name__ == "__main__":
    # Program açılırken veritabanı klasörü ve tabloları kontrol edilir
    veritabani_hazirla()
    pencere.mainloop()