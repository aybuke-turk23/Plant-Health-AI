import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os

# 1. Modeli Yükle
model_path = 'models/plant_health_mobilenet.h5'
model = tf.keras.models.load_model(model_path)
class_names = ['Biber (Pepper)', 'Patates (Potato)', 'Domates (Tomato)']

def predict_leaf(img_path):
    # Resmi yükle ve modelin istediği boyuta getir
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) # Boyut ekle (1, 224, 224, 3)

    # Tahmin yap
    predictions = model.predict(img_array)
    
    # Skorları al (Softmax zaten modelin içinde, direkt en yükseği bulalım)
    score = predictions[0] 
    result_index = np.argmax(score)
    result = class_names[result_index]
    
    # Güven oranını yüzde olarak hesapla
    confidence = 100 * score[result_index]
    
    print(f"\n--- 🌿 YAPAY ZEKA TEŞHİSİ ---")
    print(f"Resim: {os.path.basename(img_path)}")
    print(f"Sonuç: BU BİR {result.upper()} YAPRAĞI!")
    print(f"Güven Oranı: %{confidence:.2f}")

# 2. TEST RESMİ (Aynı resmi veya yeni birini dene)
# farklı bilgisayarlarda çalışabilmesi için bu satır mevcut bilgisayara göre düzenlenmeli.
test_image = 'data/processed/tomato/fff3aeaf-d4ae-4f3a-86d9-79237d07270f___Com.G_SpM_FL 9349.JPG'

if os.path.exists(test_image):
    predict_leaf(test_image)
else:
    print("Resim bulunamadı!")