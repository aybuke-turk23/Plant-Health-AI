import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
import os

# 1. AYARLAR
BATCH_SIZE = 32
IMG_SIZE = (224, 224)
DATA_PATH = 'data/processed'

# 2. VERİ SETİNİ YÜKLE
# Klasörlerden resimleri okur ve %20'sini test için ayırır
print("Veriler yükleniyor...")
train_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_PATH,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_PATH,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

# 3. MOBILENETV2 (TRANSFER LEARNING) KURULUMU
# Hazır eğitilmiş modeli alıyoruz ama son katmanını kendi bitkilerimize göre değiştireceğiz
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # Mevcut zekasını donduruyoruz

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.2), # Ezberlemeyi önlemek için
    layers.Dense(3, activation='softmax') # 3 sınıf: Tomato, Potato, Pepper
])

# 4. MODELİ DERLE
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# 5. EĞİTİMİ BAŞLAT
print("\nEğitim başlıyor ")
model.fit(train_ds, validation_data=val_ds, epochs=15)

# 6. MODELİ KAYDET
if not os.path.exists('models'):
    os.makedirs('models')

model.save('models/plant_health_mobilenet.h5')
print("\n✅ Model başarıyla 'models/plant_health_mobilenet.h5' olarak kaydedildi!")