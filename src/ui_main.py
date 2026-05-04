import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import sys
import os

# 1. SET FILE PATHS (Critical for module access)
# Allows Python to access database_manager in the main directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from database_manager import veritabani_hazirla, analiz_kaydet, analizleri_listele
    from predict import predict_leaf
except ImportError as e:
    print(f"Error: Modules could not be loaded. Please check file paths.\nDetails: {e}")

image_path = ""

# 2. IMAGE SELECTION FUNCTION
def select_image():
    global image_path
    file = filedialog.askopenfilename(
        title="Select a Plant Leaf Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )

    if file:
        image_path = file
        img = Image.open(file)
        img = img.resize((250, 250))  # Resize for UI
        img = ImageTk.PhotoImage(img)
        
        label_image.config(image=img)
        label_image.image = img
        result_label.config(text="Image ready. Click analyze button!", fg="#1b5e20")

# 3. ANALYSIS AND SAVE FUNCTION (Main Engine)
def analyze():
    if not image_path:
        result_label.config(text="⚠️ Please select an image first!", fg="red")
        return

    result_label.config(text="🔍 Analyzing, please wait...", fg="#1b5e20")
    window.update()  # Prevent UI freezing

    try:
        # Run AI Model
        disease, confidence = predict_leaf(image_path)
        
        if disease:
            # Display Result
            result_text = f"🌿 Result: {disease}\n🎯 Confidence: %{confidence:.2f}"
            result_label.config(text=result_text, fg="#2e7d32")
            
            # Save to Database
            # Extract plant type from first word of prediction (e.g., Tomato)
            plant_type = disease.split()[0] 
            analiz_kaydet(plant_type, image_path, disease, confidence)
            print(f"✅ Success: {disease} saved to database.")
        else:
            result_label.config(text="❌ Prediction failed!", fg="red")

    except Exception as e:
        result_label.config(text=f"Error: {str(e)}", fg="red")

def view_history():
    # 1. Create new window
    history_window = tk.Toplevel(window)
    history_window.title("Analysis History")
    history_window.geometry("700x450")
    history_window.config(bg="#f1f8e9")

    # Title
    tk.Label(
        history_window, 
        text="📋 Saved Analysis History", 
        font=("Arial", 14, "bold"), 
        bg="#f1f8e9",
        fg="#2e7d32"
    ).pack(pady=15)

    # 2. Fetch records from database
    try:
        from database_manager import analizleri_listele
        records = analizleri_listele()
    except Exception as e:
        tk.Label(history_window, text=f"Data fetch error: {e}", fg="red").pack()
        return

    # 3. List area and scrollbar
    frame = tk.Frame(history_window, bg="#f1f8e9")
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    # Use monospace font for aligned columns
    listbox = tk.Listbox(
        frame, 
        font=("Courier New", 10), 
        width=80, 
        yscrollcommand=scrollbar.set,
        bg="white",
        relief="flat",
        borderwidth=5
    )
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=listbox.yview)

    # 4. Table headers
    header = f"{'Plant':<12} | {'Diagnosis':<20} | {'Confidence':<10} | {'Date'}"
    listbox.insert(tk.END, header)
    listbox.insert(tk.END, "-" * 75)

    # 5. Insert data (with error handling)
    if not records:
        listbox.insert(tk.END, "No analysis records found yet.")
    else:
        for row in records:
            try:
                # row structure: (id, plant_type, image_path, result, confidence, date)
                
                plant = str(row[1])
                diagnosis = str(row[3])
                date = str(row[5])
                
                raw_confidence = row[4]
                try:
                    if isinstance(raw_confidence, bytes):
                        confidence_float = float(raw_confidence.decode('utf-8'))
                    else:
                        confidence_float = float(raw_confidence)
                    confidence_str = f"{confidence_float:.2f}"
                except (ValueError, TypeError):
                    confidence_str = str(raw_confidence)

                info = f"{plant:<12} | {diagnosis:<20} | {confidence_str:<10} | {date}"
                listbox.insert(tk.END, info)
                
            except Exception as err:
                print(f"Row processing error: {err}")
                continue

    # Close button
    tk.Button(history_window, text="Close Window", command=history_window.destroy, bg="#81c784").pack(pady=10)


# 4. GUI DESIGN
window = tk.Tk()
window.title("Plant Health AI - Fırat University")
window.geometry("450x600")
window.config(bg="#f1f8e9")

title = tk.Label(
    window,
    text="🌱 Plant Health AI",
    font=("Helvetica", 22, "bold"),
    bg="#f1f8e9",
    fg="#2e7d32"
)
title.pack(pady=20)

btn_select = tk.Button(
    window,
    text="📂 Select Image",
    font=("Arial", 11),
    width=20,
    command=select_image,
    bg="white"
)
btn_select.pack(pady=10)

# Image preview area
label_image = tk.Label(window, bg="white", width=300, height=250, relief="solid")
label_image.pack(pady=10)

btn_analyze = tk.Button(
    window,
    text="🔍 Start Analysis",
    font=("Arial", 12, "bold"),
    width=20,
    bg="#4caf50",
    fg="white",
    command=analyze,
    activebackground="#388e3c"
)
btn_analyze.pack(pady=20)

btn_history = tk.Button(
    window,
    text="📋 View History",
    font=("Arial", 11),
    width=20,
    command=view_history,
    bg="#81c784",
    fg="white"
)
btn_history.pack(pady=5)

result_label = tk.Label(
    window,
    text="Analysis results will appear here",
    font=("Arial", 11, "italic"),
    bg="#f1f8e9",
    fg="#555",
    justify="center"
)
result_label.pack(pady=15)

# 5. START PROGRAM
if __name__ == "__main__":
    # Initialize database on startup
    veritabani_hazirla()
    window.mainloop()