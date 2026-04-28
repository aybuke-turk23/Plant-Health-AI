import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# MODELİ DIŞARIDA YÜKLÜYORUZ (Sistem açılırken bir kez yüklenir)
model = tf.keras.models.load_model('models/plant_health_mobilenet.h5')
class_names = ['Pepper', 'Potato', 'Tomato']

# TÜM TAHMİN MANTIĞI BU FONKSİYONUN İÇİNDE
def predict_leaf(img_path):
    try:
        # 1. Resim Hazırlığı
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0  # Normalizasyon burada
        img_array = tf.expand_dims(img_array, 0)

        # 2. Tahmin Alma
        predictions = model.predict(img_array)
        
        # 3. Sonuçları Ayıklama
        score = predictions[0]
        result_class = class_names[np.argmax(score)]
        confidence = 100 * np.max(score)

        return result_class, confidence

    except Exception as e:
        print(f"Hata: {e}")
        return None, None

# BURASI TEST İÇİN (Arayüzde çalışırken burası devreye girmez)
if __name__ == "__main__":
    # Test için bilgisayarından bir resim yolu ver
    resim = r'C:\Users\lenovo\OneDrive\Desktop\PlantHealth-AI\Plant-Health-AI\data\raw\tomato\Tomato_Bacterial_spot\0a1655ed-797c-4d1d-ba35-dc255d68a2ee___GCREC_Bact.Sp 3560.JPG' 
    sonuc, oran = predict_leaf(resim)
    print(f"Sonuç: {sonuc} - Güven: %{oran:.2f}")
