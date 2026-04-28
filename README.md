   ## 🌿  Plant-Health-AI
👋Hi! This is our software engineering project.We use Artificial Intelligence System to find diseases in plant leafs with MobileNetV2.

## 📝 About Project:
We use Python and Deep Learning .  
For now ; we focus on 3 plants: which is ; Tomato, Pepper, Potato  
We aim to our AI can see if the leaf health or sick.  

## 🪛 How to Start:
1.Clone the repository.  

   git clone [link]  
   
2.Install libraries:  

  pip install -r requirements.txt  
  
3.Get data from.  

  Download data.zip from Google drive link.(Data link is shared within the team. )  
  Or:  
  https://www.kaggle.com/datasets/emmarex/plantdisease 

## 📁 AboutFolders:

src/: our python codes 

data/raw/ : leaf images(original versions)  

data/processed/ : resized images (224x224) for AI.  

models/ : our AI models files.(.h5)  

## ⚙️ How to Run
 for prepareing the images:  
    python src/preprocessing.py  
    
 start the application:(Working on it !!)  
    python src/main.py

## 🖥️ Tech Stack:  
for Deep learning; TensorFlow&Keras  
Architecture; MobileNetV2  
Database;SQLite  

  

