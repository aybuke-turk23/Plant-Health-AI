import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# 1. Modeli Yükle
model = tf.keras.models.load_model('models/plant_health_mobilenet.h5')
class_names = ['Pepper', 'Potato', 'Tomato'] # Klasör sırasına göre

# 2. Test Edilecek Resmi Yükle (Buraya bir resim yolu yazmalısın)
img_path = 'data/raw/tomato/bir_resim_adi.jpg' # Denemek istediğin bir resmin yolunu yaz
img = image.load_img(img_path, target_size=(224, 224))

# 3. Tahmin Et
img_array = image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) 

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

print(f"Bu bir {class_names[np.argmax(score)]} yaprağı! (Güven oranı: %{100 * np.max(score):.2f})")