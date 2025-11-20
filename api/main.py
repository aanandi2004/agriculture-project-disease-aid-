# main.py
import os
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv

import requests
import numpy as np
from io import BytesIO
from PIL import Image

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import tensorflow as tf
from tensorflow.keras.applications.efficientnet_v2 import preprocess_input

# local treatments.py (your file)
from treatments import treatments

# -----------------------
# Config + logging
# -----------------------
load_dotenv()  # load local .env in development
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agri-api")

OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"  # 5 day / 3 hour

# -----------------------
# FastAPI app + CORS
# -----------------------
app = FastAPI(title="AgriAid - Disease Detection API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Helpers: model loading
# -----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_model_safe(path: str):
    """Load a Keras model if present, otherwise return None (and log)."""
    try:
        if not os.path.exists(path):
            logger.warning("Model file not found: %s", path)
            return None
        model = tf.keras.models.load_model(path)
        logger.info("Loaded model: %s", path)
        return model
    except Exception as e:
        logger.exception("Failed to load model %s: %s", path, e)
        return None


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# saved_models folder inside api
MODEL_DIR = os.path.join(BASE_DIR, "saved_models")

POTATO_MODEL = load_model_safe(os.path.join(MODEL_DIR, "potato_v1.keras"))
TOMATO_MODEL = load_model_safe(os.path.join(MODEL_DIR, "tomato_v1.keras"))
PEPPER_MODEL = load_model_safe(os.path.join(MODEL_DIR, "pepper_v1.keras"))
RICE_MODEL = load_model_safe(os.path.join(MODEL_DIR, "rice_v1.keras"))
# -----------------------
# Class labels (must match training order)
# -----------------------
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

# -----------------------
# Image preprocessing helpers
# -----------------------
def preprocess_256(img_bytes: bytes) -> np.ndarray:
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    img = img.resize((256, 256))
    arr = np.array(img).astype(np.float32) / 255.0
    arr = np.expand_dims(arr, 0)
    return arr


def preprocess_rice(img_bytes: bytes) -> np.ndarray:
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    img = img.resize((224, 224))
    arr = np.array(img).astype(np.float32)
    arr = np.expand_dims(arr, 0)
    arr = preprocess_input(arr)  # EfficientNet preprocessing
    return arr


# -----------------------
# Weather helpers
# -----------------------
_geocode_cache: Dict[str, Dict[str, float]] = {}


def geocode_location(location: str) -> Optional[Dict[str, float]]:
    """Return {'lat': float, 'lon': float} or None. Uses OpenWeather geocoding."""
    if not OPENWEATHER_API_KEY:
        return None
    key = location.strip().lower()
    if key in _geocode_cache:
        return _geocode_cache[key]
    params = {"q": location, "limit": 1, "appid": OPENWEATHER_API_KEY}
    try:
        r = requests.get(GEOCODE_URL, params=params, timeout=8)
        r.raise_for_status()
        data = r.json()
        if not data:
            return None
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        _geocode_cache[key] = {"lat": lat, "lon": lon}
        return {"lat": lat, "lon": lon}
    except Exception as e:
        logger.warning("Geocode failed for %s: %s", location, e)
        return None


def fetch_5day_forecast(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    if not OPENWEATHER_API_KEY:
        return None
    params = {"lat": lat, "lon": lon, "units": "metric", "appid": OPENWEATHER_API_KEY}
    try:
        r = requests.get(FORECAST_URL, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.warning("Forecast fetch failed for %s,%s: %s", lat, lon, e)
        return None


def analyze_forecast_and_recommend(forecast_json: dict, days: int = 3) -> Dict[str, Any]:
    if not forecast_json or "list" not in forecast_json:
        return {"rain_mm": None, "max_pop": None, "avg_humidity": None, "recommendation": "No weather data."}
    entries = forecast_json["list"]
    entries_needed = min(len(entries), days * 8)
    entries = entries[:entries_needed]

    rain_sum = 0.0
    pops = []
    hums = []

    for ent in entries:
        # rain in 3-hour bucket
        if "rain" in ent:
            rain_sum += float(ent["rain"].get("3h", 0.0))
        pop = ent.get("pop")
        if pop is not None:
            pops.append(float(pop))
        hum = ent.get("main", {}).get("humidity")
        if hum is not None:
            hums.append(float(hum))

    max_pop = max(pops) if pops else None
    avg_humidity = (sum(hums) / len(hums)) if hums else None

    # simple rules
    if rain_sum >= 10:
        recommendation = (
            f"Heavy rain (~{rain_sum:.1f} mm over next {days} days). Chemical sprays may wash off; recommend waiting 3–4 days."
        )
    elif max_pop is not None and max_pop >= 0.6:
        recommendation = f"High chance of rain (peak {max_pop:.0%}). Prefer organic or delay chemical spray."
    elif avg_humidity is not None and avg_humidity >= 85:
        recommendation = f"Very high humidity (~{avg_humidity:.0f}%) — conditions favor disease. Consider preventive treatment."
    else:
        recommendation = "Weather suitable for application now."

    return {
        "rain_mm": round(rain_sum, 2),
        "max_pop": round(max_pop, 2) if max_pop is not None else None,
        "avg_humidity": round(avg_humidity, 1) if avg_humidity is not None else None,
        "recommendation": recommendation,
    }


# -----------------------
# Endpoints
# -----------------------
@app.get("/ping")
async def ping():
    return {"message": "server active"}


@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    crop_type: str = Form(...),
    location: Optional[str] = Form(None),  # optional: lat,lon or city/district
):
    """
    Predict disease from image. If 'location' provided, also return weather advice.
    location can be "city", "city, country" OR "lat,lon" (e.g. "19.07,72.87").
    """

    crop_type = crop_type.strip().lower()
    img_bytes = await file.read()

    # pick model + preprocessing
    if crop_type == "potato":
        model = POTATO_MODEL
        class_names = POTATO_CLASSES
        img_batch = preprocess_256(img_bytes)
    elif crop_type == "tomato":
        model = TOMATO_MODEL
        class_names = TOMATO_CLASSES
        img_batch = preprocess_256(img_bytes)
    elif crop_type == "pepper":
        model = PEPPER_MODEL
        class_names = PEPPER_CLASSES
        img_batch = preprocess_256(img_bytes)
    elif crop_type == "rice":
        model = RICE_MODEL
        class_names = RICE_CLASSES
        img_batch = preprocess_rice(img_bytes)
    else:
        raise HTTPException(status_code=400, detail="Invalid crop_type (use potato/tomato/pepper/rice)")

    if model is None:
        # helpful message — model not present on server
        raise HTTPException(status_code=500, detail=f"Model for '{crop_type}' not available on server. Add model file to saved_models/ and restart.")

    # run prediction
    try:
        preds = model.predict(img_batch)
        idx = int(np.argmax(preds[0]))
        confidence = float(np.max(preds[0]))
        predicted_class = class_names[idx]
    except Exception as e:
        logger.exception("Prediction failed: %s", e)
        raise HTTPException(status_code=500, detail="Model prediction failed")

    # lookup treatment (safe access)
    disease_key = predicted_class.strip().lower().replace(" ", "_")
    treatment_info = {"organic": [], "chemical": []}
    crop_dict = treatments.get(crop_type, {}) if isinstance(treatments, dict) else {}
    if isinstance(crop_dict, dict) and disease_key in crop_dict and isinstance(crop_dict[disease_key], dict):
        treatment_info = crop_dict[disease_key]

    # weather analysis (optional)
    weather_summary = None
    if location:
        # try lat,lon input first
        loc_coords = None
        if "," in location:
            try:
                lat_s, lon_s = location.split(",")
                loc_coords = {"lat": float(lat_s.strip()), "lon": float(lon_s.strip())}
            except Exception:
                loc_coords = None
        if loc_coords is None:
            loc_coords = geocode_location(location)
        if loc_coords:
            forecast_json = fetch_5day_forecast(loc_coords["lat"], loc_coords["lon"])
            weather_summary = analyze_forecast_and_recommend(forecast_json, days=3)
            weather_summary["lat"] = loc_coords["lat"]
            weather_summary["lon"] = loc_coords["lon"]
            # disease-specific override (if weather_rules exist)
            disease_rules = {}
            if isinstance(crop_dict, dict) and disease_key in crop_dict and isinstance(crop_dict[disease_key], dict):
                disease_rules = crop_dict[disease_key].get("weather_rules", {})
            # apply disease thresholds if provided
            try:
                rain_th = disease_rules.get("heavy_rain_mm")
                hum_th = disease_rules.get("humidity_high_pct")
                if rain_th is not None and weather_summary.get("rain_mm") is not None:
                    if weather_summary["rain_mm"] >= rain_th:
                        weather_summary["recommendation"] = (
                            f"Based on disease-specific rule (rain >= {rain_th} mm) heavy rain expected; delay chemical spraying."
                        )
                if hum_th is not None and weather_summary.get("avg_humidity") is not None:
                    if weather_summary["avg_humidity"] >= hum_th:
                        weather_summary["recommendation"] = (
                            f"Based on disease-specific rule (humidity >= {hum_th}%) high humidity detected; consider preventive steps."
                        )
            except Exception:
                # don't crash due to unexpected structure
                logger.exception("Error applying disease-specific weather rules")

    response = {
        "crop_type": crop_type,
        "predicted_class": predicted_class,
        "confidence": confidence,
        "treatment_info": treatment_info,
        "weather_forecast": weather_summary,
    }
    return response


@app.get("/treatment/{predicted_class}")
async def get_treatment(predicted_class: str):
    """Return stored treatment info for a disease key (case-insensitive)."""
    disease_key = predicted_class.strip().lower().replace(" ", "_")
    if not isinstance(treatments, dict):
        raise HTTPException(status_code=500, detail="Treatments data not available")
    for crop_name, crop_map in treatments.items():
        if not isinstance(crop_map, dict):
            continue
        if disease_key in crop_map and isinstance(crop_map[disease_key], dict):
            return {"disease": predicted_class, "treatment_info": crop_map[disease_key]}
    raise HTTPException(status_code=404, detail="Treatment not found")
