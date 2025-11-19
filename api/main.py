# main.py
import os
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.efficientnet_v2 import preprocess_input

from treatments import treatments

# ========================
# Load .env (local dev)
# ========================
load_dotenv()

# ========================
# OpenWeather config
# ========================
OWM_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"  # 5 day / 3 hour

# ========================
# App init & CORS
# ========================
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================
# Load models (update paths if needed)
# ========================
POTATO_MODEL = tf.keras.models.load_model(
    r"C:\Users\Admin\Documents\jupyter notebook\crop disease detection\potato disease\saved_models\1.keras"
)
TOMATO_MODEL = tf.keras.models.load_model(
    r"C:\Users\Admin\Documents\jupyter notebook\crop disease detection\potato disease\saved_models\tomato_v1.keras"
)
PEPPER_MODEL = tf.keras.models.load_model(
    r"C:\Users\Admin\Documents\jupyter notebook\crop disease detection\potato disease\saved_models\pepper_v1.keras"
)
RICE_MODEL = tf.keras.models.load_model(
    r"C:\Users\Admin\Documents\jupyter notebook\crop disease detection\potato disease\saved_models\rice_v1.keras"
)

# ========================
# Class labels (must match model training)
# ========================
POTATO_CLASSES = ["Early blight", "Late blight", "Healthy"]
TOMATO_CLASSES = [
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite",
    "Tomato_Target_Spot",
    "Tomato_Tomato_YellowLeaf_Curl_Virus",
    "Tomato_Tomato_mosaic_virus",
    "Tomato_healthy",
]
PEPPER_CLASSES = ["Pepper__bell_Bacterial_spot", "Pepper__bell_healthy"]
RICE_CLASSES = [
    "bacterial_leaf_blight",
    "bacterial_leaf_streak",
    "bacterial_panicle_blight",
    "blast",
    "brown_spot",
    "dead_heart",
    "downy_mildew",
    "hispa",
    "normal",
    "tungro",
]

# ========================
# Preprocessing helpers
# ========================
def preprocess_256(img_bytes: bytes) -> np.ndarray:
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    img = img.resize((256, 256))
    arr = np.array(img) / 255.0
    arr = np.expand_dims(arr, 0).astype(np.float32)
    return arr

def preprocess_rice(img_bytes: bytes) -> np.ndarray:
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    img = img.resize((224, 224))
    arr = np.array(img).astype(np.float32)
    arr = np.expand_dims(arr, 0)
    arr = preprocess_input(arr)
    return arr

# ========================
# Weather helpers (Geocoding + Forecast)
# Using OpenWeather 5-day / 3-hour forecast (free)
# ========================
_geocode_cache: Dict[str, Dict[str, float]] = {}

def geocode_location(location: str) -> Optional[Dict[str, float]]:
    """Return {'lat': float, 'lon': float} or None."""
    if not OWM_API_KEY:
        return None
    loc_key = location.strip().lower()
    if loc_key in _geocode_cache:
        return _geocode_cache[loc_key]
    params = {"q": location, "limit": 1, "appid": OWM_API_KEY}
    try:
        r = requests.get(GEOCODE_URL, params=params, timeout=8)
        r.raise_for_status()
        data = r.json()
        if not data:
            return None
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        _geocode_cache[loc_key] = {"lat": lat, "lon": lon}
        return {"lat": lat, "lon": lon}
    except Exception:
        return None

def fetch_5day_forecast(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    """Call 5-day/3-hour OpenWeather forecast and return parsed JSON or None."""
    if not OWM_API_KEY:
        return None
    params = {"lat": lat, "lon": lon, "units": "metric", "appid": OWM_API_KEY}
    try:
        r = requests.get(FORECAST_URL, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

def analyze_forecast_and_recommend(forecast_json: dict, days: int = 3) -> dict:
    """
    Use 5-day/3-hour forecast entries (list of ~40 items).
    Sum rain (from 'rain'->'3h') over next `days` days (approx days*8 entries).
    Compute avg humidity and peak pop (if provided).
    Return summary + recommendation text based on simple rules.
    """
    if not forecast_json or "list" not in forecast_json:
        return {"rain_mm": None, "max_pop": None, "avg_humidity": None, "recommendation": "Weather data not available."}

    entries = forecast_json["list"]
    # approx number of 3-hour entries to cover `days` days
    entries_needed = min(len(entries), days * 8)  # 8 entries per day
    entries = entries[:entries_needed]

    rain_sum = 0.0
    pops = []
    hums = []
    for ent in entries:
        # rainfall in 3-hour bucket often under ent['rain']['3h']
        rain_val = 0.0
        if "rain" in ent:
            rain_val = float(ent["rain"].get("3h", 0.0))
        rain_sum += rain_val

        # probability of precipitation might exist (0..1)
        pop = ent.get("pop", None)
        if pop is not None:
            pops.append(float(pop))

        # humidity is in ent['main']['humidity']
        main = ent.get("main", {})
        hum = main.get("humidity", None)
        if hum is not None:
            hums.append(float(hum))

    max_pop = max(pops) if pops else None
    avg_humidity = (sum(hums) / len(hums)) if hums else None

    # Decision rules (tunable)
    # heavy rain threshold: >= 10 mm over next `days`
    if rain_sum >= 10:
        recommendation = (
            f"Heavy rain expected (~{rain_sum:.1f} mm in next {days} days). "
            "Chemical spraying now may be washed off — recommend waiting 3–4 days after rain subsides. "
            "Consider organic/bio-control if immediate action is necessary."
        )
    elif max_pop is not None and max_pop >= 0.6:
        recommendation = (
            f"High probability of precipitation (peak {max_pop:.0%}) in next {days} days. "
            "Prefer organic or delay chemical spray."
        )
    elif avg_humidity is not None and avg_humidity >= 85:
        recommendation = (
            f"Very high humidity (~{avg_humidity:.0f}%) which favors fungal spread. "
            "Apply preventive treatment (follow chemical/organic prevention instructions) as soon as possible."
        )
    else:
        recommendation = "Weather suitable for application now."

    return {
        "rain_mm": round(rain_sum, 2),
        "max_pop": round(max_pop, 2) if max_pop is not None else None,
        "avg_humidity": round(avg_humidity, 1) if avg_humidity is not None else None,
        "recommendation": recommendation,
    }

# ========================
# Endpoints
# ========================
@app.get("/ping")
async def ping():
    return {"message": "Server Active 🚀"}

@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    crop_type: str = Form(...),
    location: str = Form(...)  # MANDATORY per your choice (Option B)
):
    # 1) validate API key presence
    if not OWM_API_KEY:
        raise HTTPException(status_code=500, detail="OPENWEATHER_API_KEY not configured on server.")

    crop_type = crop_type.lower()
    img_bytes = await file.read()

    # 2) choose preprocessing + model
    if crop_type == "potato":
        img_batch = preprocess_256(img_bytes)
        model = POTATO_MODEL
        class_names = POTATO_CLASSES
    elif crop_type == "tomato":
        img_batch = preprocess_256(img_bytes)
        model = TOMATO_MODEL
        class_names = TOMATO_CLASSES
    elif crop_type == "pepper":
        img_batch = preprocess_256(img_bytes)
        model = PEPPER_MODEL
        class_names = PEPPER_CLASSES
    elif crop_type == "rice":
        img_batch = preprocess_rice(img_bytes)
        model = RICE_MODEL
        class_names = RICE_CLASSES
    else:
        raise HTTPException(status_code=400, detail="Invalid crop type! Use potato, tomato, pepper, or rice.")

    # 3) predict
    preds = model.predict(img_batch)
    idx = int(np.argmax(preds[0]))
    confidence = float(np.max(preds[0]))
    predicted_class = class_names[idx]

    # 4) treatment info
    disease_key = predicted_class.lower().replace(" ", "_")
    treatment_info = {"organic": [], "chemical": []}
    if crop_type in treatments and disease_key in treatments[crop_type]:
        treatment_info = treatments[crop_type][disease_key]

    # 5) resolve location -> lat/lon (mandatory)
    loc = None
    # allow direct lat,lon input
    if "," in location:
        try:
            lat_s, lon_s = location.split(",")
            loc = {"lat": float(lat_s.strip()), "lon": float(lon_s.strip())}
        except Exception:
            loc = None

    if loc is None:
        loc = geocode_location(location)
    if loc is None:
        raise HTTPException(status_code=400, detail="Could not resolve location to coordinates. Please send valid city/district or lat,lon.")

    # 6) fetch forecast and analyze (next 3 days)
    forecast_json = fetch_5day_forecast(loc["lat"], loc["lon"])
    weather_summary = analyze_forecast_and_recommend(forecast_json, days=3)
    weather_summary["lat"] = loc["lat"]
    weather_summary["lon"] = loc["lon"]

    # 7) If disease has weather_rules, we can tailor recommendation text further
    disease_rules = {}
    if crop_type in treatments and disease_key in treatments[crop_type]:
        disease_rules = treatments[crop_type][disease_key].get("weather_rules", {})

    # optionally augment recommendation based on disease-specific thresholds
    h_rain_th = disease_rules.get("heavy_rain_mm", None)
    h_hum_th = disease_rules.get("humidity_high_pct", None)

    # If specific thresholds exist, override generic message when triggered
    if weather_summary.get("rain_mm") is not None and h_rain_th is not None:
        if weather_summary["rain_mm"] >= h_rain_th:
            weather_summary["recommendation"] = (
                f"Based on disease-specific rules (threshold {h_rain_th} mm), heavy rain (~{weather_summary['rain_mm']} mm) expected. "
                "Delay chemical spraying 3–4 days."
            )
    if weather_summary.get("avg_humidity") is not None and h_hum_th is not None:
        if weather_summary["avg_humidity"] >= h_hum_th:
            weather_summary["recommendation"] = (
                f"Based on disease-specific rules (humidity >= {h_hum_th}%), high humidity (~{weather_summary['avg_humidity']}%) detected. "
                "Apply preventive treatment as soon as possible."
            )

    # 8) Build final response
    response = {
        "crop_type": crop_type,
        "predicted_class": predicted_class,
        "confidence": confidence,
        "treatment_info": treatment_info,
        "weather_forecast": weather_summary,
    }

    return response

# ========================
# Treatment lookup endpoint (unchanged)
# ========================
@app.get("/treatment/{predicted_class}")
async def get_treatment(predicted_class: str):
    disease_key = predicted_class.lower().replace(" ", "_")
    for crop in treatments:
        if disease_key in treatments[crop]:
            return {"disease": predicted_class, "treatment_info": treatments[crop][disease_key]}
    raise HTTPException(status_code=404, detail="Treatment not found")
