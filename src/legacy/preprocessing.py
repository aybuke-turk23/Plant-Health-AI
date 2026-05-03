import cv2
import os

def preprocess_images(input_base_path, output_base_path, size=(224, 224)):
    categories = ['pepper', 'potato', 'tomato']
    
    for category in categories:
        input_category_path = os.path.join(input_base_path, category)
        output_category_path = os.path.join(output_base_path, category)
        
        if not os.path.exists(input_category_path):
            continue

        print(f"\n--- {category.upper()} İşleniyor ---")
        count = 0

        # os.walk kullanarak tüm alt klasörlerdeki resimleri buluyoruz
        for root, dirs, files in os.walk(input_category_path):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(root, file)
                    img = cv2.imread(img_path)
                    
                    if img is not None:
                        # Resizing
                        resized = cv2.resize(img, size)
                        
                        # Processed altında ana kategori klasörünü oluştur
                        if not os.path.exists(output_category_path):
                            os.makedirs(output_category_path)
                        
                        # Kaydet (Tüm alt klasörlerdeki resimleri tek bir ana kategoride toplar)
                        cv2.imwrite(os.path.join(output_category_path, file), resized)
                        count += 1
                        
                        if count % 100 == 0:
                            print(f"{count} resim işlendi...")

        print(f"Bitti! {category} kategorisinde toplam {count} resim işlendi.")

if __name__ == "__main__":
    preprocess_images("data/raw", "data/processed")