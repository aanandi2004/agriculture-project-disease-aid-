# 🌾 AI-Powered Crop Disease Detection & Weather-Aware Treatment System

This is an AI-based crop disease detection system that uses deep learning models to classify plant diseases from images of leaves.  
It also provides **organic & chemical treatments**, **prevention methods**, and **weather-aware recommendations** using real-time weather APIs.

This system currently supports:

- 🥔 Potato  
- 🍅 Tomato  
- 🫑 Pepper  
- 🌾 Rice (EfficientNet-based model)

---

## 🚀 Features

### 🔍 **1. AI Disease Detection**
Upload a leaf image and select crop type.  
The backend runs a trained TensorFlow model to predict the disease.

### 💊 **2. Treatment Recommendation**
For each disease, the system provides:
- Organic treatment  
- Chemical treatment  
- Dosage  
- Prevention tips  

(All stored in `treatments.py`.)

### 🌦️ **3. Weather-Aware Advisory**
AgriAid uses **OpenWeather API** to check rainfall/humidity forecasts and recommends:

- Whether to apply organic or chemical treatment  
- Whether to **delay spraying** due to bad weather  
- Whether conditions are ideal for fungal infection spread  

### ⚡ **4. FastAPI Backend**
Fast, scalable API with endpoints:
- `/predict`
- `/treatment/{disease}`
- `/weather-advice`

### 🖼️ **5. Supports Multiple Deep Learning Models**
- Rice → EfficientNet-V2 (224×224 preprocessing)  
- Others → Custom CNN models (256×256 preprocessing)

---

## 📂 Project Structure

project/
│── api/
│ ├── main.py # FastAPI backend
│ ├── treatments.py # Disease treatments database
│ ├── .env # API keys (NOT pushed to GitHub)
│ ├── requirements.txt # Dependencies
│
│── saved_models/ # All .keras models (ignored in Git)
│
│── frontend/ # Web app / UI (React or HTML)
│
│── training/ # Jupyter notebooks & training code
│
└── README.md

yaml
Copy code

---

## 🔧 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/agraid.git
cd agraid/api
2️⃣ Create a Virtual Environment
bash
Copy code
python -m venv venv
venv\Scripts\activate       # Windows
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
🔑 Environment Variables
Create a file named .env inside api/:

ini
Copy code
WEATHER_API_KEY=your_openweather_api_key_here
⚠️ Never upload .env to GitHub (it is already in .gitignore).

▶️ Running the Backend
bash
Copy code
uvicorn main:app --reload
Now open:

➤ API Docs: http://127.0.0.1:8000/docs
➤ Health check: http://127.0.0.1:8000/ping

🧪 API Endpoints
POST /predict
Predict disease from a leaf image.

GET /treatment/{disease}
Get organic + chemical + prevention treatment.

GET /weather-advice
Get weather-based recommendation for spraying.

🌐 Deployment
Recommended backend hosting options:

Railway.app (best for FastAPI)

Render.com

Deta Space

Azure/AWS/GCP (advanced)

Frontend can be hosted on:

Vercel

Netlify

GitHub Pages

NOTE: Your .keras models MUST be uploaded to cloud storage (Google Drive, AWS S3, etc.) if host memory is small.

📜 License
MIT License © 2025 YOUR NAME

👨‍💻 Author
Developed by Aarya and Aditya
For academic + real-world agricultural applications.