import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

resim_yolu = ""

def resim_sec():
    global resim_yolu
    dosya = filedialog.askopenfilename()

    if dosya:
        resim_yolu = dosya
        img = Image.open(dosya)
        img = img.resize((250, 250))

        img = ImageTk.PhotoImage(img)
        label_resim.config(image=img)
        label_resim.image = img

        sonuc_label.config(text="Resim seçildi")

def analiz_et():
    if resim_yolu == "":
        sonuc_label.config(text="Lütfen önce resim seç")
    else:
        # şimdilik sahte sonuç
        sonuc_label.config(
            text="🌿 Bitki: Domates\nDurum: Sağlıklı\nGüven: %95"
        )

pencere = tk.Tk()
pencere.title("Plant Health AI")
pencere.geometry("450x550")
pencere.config(bg="#e8f5e9")

baslik = tk.Label(
    pencere,
    text="🌱 Plant Health AI",
    font=("Arial", 20, "bold"),
    bg="#e8f5e9",
    fg="#1b5e20"
)
baslik.pack(pady=15)

btn_sec = tk.Button(
    pencere,
    text="📂 Resim Seç",
    font=("Arial", 12),
    width=20,
    command=resim_sec
)
btn_sec.pack(pady=10)

label_resim = tk.Label(pencere, bg="white", width=300, height=250)
label_resim.pack(pady=10)

btn_analiz = tk.Button(
    pencere,
    text="🔍 Analiz Et",
    font=("Arial", 12, "bold"),
    width=20,
    bg="#4caf50",
    fg="white",
    command=analiz_et
)
btn_analiz.pack(pady=15)

sonuc_label = tk.Label(
    pencere,
    text="Sonuç burada görünecek",
    font=("Arial", 12),
    bg="#e8f5e9",
    justify="center"
)
sonuc_label.pack(pady=20)

pencere.mainloop()
