# 🌾 AgriAid – AI-Powered Crop Disease Detection & Weather-Aware Treatment System

AgriAid is an AI-based crop disease detection system that uses deep learning models to classify plant diseases from images of leaves.  
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

