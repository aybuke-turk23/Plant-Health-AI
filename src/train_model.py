import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
import os

# 1. AYARLAR
BATCH_SIZE = 32
IMG_SIZE = (224, 224)
DATA_PATH = 'data/raw'

# 2. VERİ SETİNİ YÜKLE
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

# KANKA BURASI KRİTİK: Sınıf isimlerini ve sayısını alıyoruz
class_names = train_ds.class_names
num_classes = len(class_names)
print(f"\n✅ {num_classes} farklı sınıf eğitilecek.")

# 3. MODEL KURULUMU
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False

model = models.Sequential([
    layers.Rescaling(1./255), # Normalizasyon eklendi
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.2),
    layers.Dense(num_classes, activation='softmax') # Dinamik sınıf sayısı
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# 5. EĞİTİM
print("\n🚀 Eğitim Başlıyor...")
model.fit(train_ds, validation_data=val_ds, epochs=15)

# 6. MODELİ VE ETİKETLERİ KAYDET
if not os.path.exists('models'): os.makedirs('models')
model.save('models/plant_health_mobilenet.h5')

# KANKA: Sınıf isimlerini bir yere kaydetmezsek predict yaparken sıralamayı karıştırırız!
with open('models/classes.txt', 'w') as f:
    for item in class_names:
        f.write("%s\n" % item)

print("\n✅ Eğitim bitti, model ve etiketler kaydedildi!")