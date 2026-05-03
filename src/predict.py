import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# MODELİ YÜKLE
model = tf.keras.models.load_model('models/plant_health_mobilenet.h5')

# Bu liste sırası, klasörlerin tam alfabetik sırasıdır. 
# Eğitimde kullanılan sırayla birebir aynı olmalı!
class_names = [
    'Pepper__bell___Bacterial_spot',
    'Pepper__bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Tomato_Bacterial_spot',
    'Tomato_Early_blight',
    'Tomato_Late_blight',
    'Tomato_Leaf_Mold',
    'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite',
    'Tomato__Target_Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus',
    'Tomato__Tomato_mosaic_virus',
    'Tomato_healthy'
]

def predict_leaf(img_path):
    try:
        # 1. Resim Hazırlığı
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        

        
        img_array = tf.expand_dims(img_array, 0)

        # 2. Tahmin Alma
        predictions = model.predict(img_array)
        
        # 3. Sonuçları Ayıklama
        score = predictions[0]
        
        # Hangi sınıf olduğunu bul
        class_index = np.argmax(score)
        result_class = class_names[class_index]
        confidence = 100 * np.max(score)

        return result_class, confidence

    except Exception as e:
        print(f"Hata: {e}")
        return None, None

if __name__ == "__main__":
    # Test için buradan bir resim ver
    resim = r'VERİ_SETİNDEN_FARKLI_BİR_RESİM_YOLU_BURAYA' 
    sonuc, oran = predict_leaf(resim)
    print(f"Sonuç: {sonuc} - Güven: %{oran:.2f}")