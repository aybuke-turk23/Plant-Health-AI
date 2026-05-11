# 🌿 Plant-Health-AI

> An AI-powered web application that analyzes plant leaf photos to detect diseases and provide expert treatment recommendations via a built-in chatbot.

---

## 📌 About the Project

Plant-Health-AI is a software engineering project that combines computer vision and large language models to help users identify plant diseases instantly.

- Upload a photo of a plant leaf
- The **Plant.id API** analyzes the image and detects potential diseases
- **Google Gemini AI** generates personalized treatment recommendations
- A built-in **AI chatbot assistant** allows follow-up questions after each analysis

---

## 🖥️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Web Framework | Flask |
| API Structure | RESTful API |
| Plant Analysis | Plant.id API v3 |
| AI Recommendations | Google Gemini 2.5 Flash |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Security | Rate limiting, file validation |

---

## 📁 Project Structure

```
Plant-Health-AI/
├── main.py                  # Flask server — /api/analyze and /api/chat endpoints
├── requirements.txt
├── .env                     # API keys (never commit this)
├── analysis_history.log     # Auto-generated analysis log
├── uploads/                 # Temporary image storage
└── src/
    ├── backend/
    │   ├── api_service.py       # Plant.id + Gemini integration
    │   └── security_manager.py  # Rate limiting and file validation
    └── frontend/
        ├── index.html
        ├── app.js               # Analysis logic + chatbot
        └── css/
            └── style.css
```

---

## ⚙️ How to Run

### 1. Clone the Repository

```bash
git clone [repository-link]
cd Plant-Health-AI
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS / Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the project root:

```env
PLANT_ID_API_KEY=your_plant_id_key_here
GEMINI_API_KEY=your_gemini_key_here
```

- **Plant.id API key** → [plant.id](https://plant.id)
- **Gemini API key** → [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

### 5. Start the Application

```bash
python main.py
```

Visit **http://127.0.0.1:5000** in your browser.

---

## 🚀 Features

- 📷 **Image Upload** — drag & drop or click to select (JPG, PNG, up to 5MB)
- 🔬 **Disease Detection** — powered by Plant.id API v3
- 📊 **Health Score** — visual ring chart showing plant health percentage
- 🤖 **AI Recommendations** — Gemini generates treatment steps after each analysis
- 💬 **Interactive Chatbot** — ask follow-up questions in the assistant panel; conversation history is maintained per session
- 🛡️ **Security Layer** — rate limiting (10s cooldown) and file type/size validation

---

## 🔒 Security Notes

- `.env` is listed in `.gitignore` — API keys are never committed
- Only `.jpg`, `.jpeg`, and `.png` files are accepted
- Maximum file size: 5MB
- Requests are rate-limited to prevent API abuse

---

## 📦 Requirements

Key dependencies (see `requirements.txt` for full list):

```
flask
flask-cors
requests
python-dotenv
google-genai
```
