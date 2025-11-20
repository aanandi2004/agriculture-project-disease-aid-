# treatments.py

treatments = {

# ============================================================
# POTATO
# ============================================================
"potato": {

    "early_blight": {
        "organic": [{
            "cure": "Neem oil spray, Bacillus subtilis, garlic extract solution.",
            "dosage": "Neem oil: 2-4 ml/L water, spray weekly.",
            "prevention": "Rotate crops, remove infected leaves, avoid overhead watering."
        }],
        "chemical": [{
            "cure": "Chlorothalonil, Mancozeb, Azoxystrobin.",
            "dosage": "Chlorothalonil: 2g/L, Mancozeb: 2.5g/L.",
            "prevention": "Apply preventatively during humid weather."
        }],
        "weather_rules": {
            "heavy_rain_mm": 10,
            "humidity_high_pct": 85
        }
    },

    "late_blight": {
        "organic": [{
            "cure": "Copper fungicide or compost tea spray.",
            "dosage": "Copper oxychloride: 2.5g/L.",
            "prevention": "Improve airflow and remove infected plants."
        }],
        "chemical": [{
            "cure": "Mancozeb or Chlorothalonil.",
            "dosage": "Mancozeb: 2.5g/L every 10 days.",
            "prevention": "Maintain consistent spray schedule."
        }],
        "weather_rules": {
            "heavy_rain_mm": 8,
            "humidity_high_pct": 90
        }
    },

    "healthy": {
        "organic": [{"cure": "No treatment required.", "dosage": "-", "prevention": "Continue regular monitoring."}],
        "chemical": [{"cure": "-", "dosage": "-", "prevention": "-"}],
        "weather_rules": {}
    }
},

# ============================================================
# TOMATO
# ============================================================
"tomato": {

    "tomato_bacterial_spot": {
        "organic": [{
            "cure": "Neem oil spray and copper-based biofungicide.",
            "dosage": "Neem oil: 3ml/L weekly.",
            "prevention": "Use certified seeds and avoid leaf wetting."
        }],
        "chemical": [{
            "cure": "Copper hydroxide or Streptomycin.",
            "dosage": "As per label.",
            "prevention": "Rotate crops and apply at first symptoms."
        }],
        "weather_rules": {"heavy_rain_mm": 12, "humidity_high_pct": 80}
    },

    "tomato_early_blight": {
        "organic": [{
            "cure": "Neem oil or compost tea spray.",
            "dosage": "Neem oil: 3ml/L every 7 days.",
            "prevention": "Proper spacing and pruning."
        }],
        "chemical": [{
            "cure": "Mancozeb or Difenoconazole.",
            "dosage": "As per instructions.",
            "prevention": "Prevent during humid periods."
        }],
        "weather_rules": {"heavy_rain_mm": 10, "humidity_high_pct": 85}
    },

    "tomato_late_blight": {
        "organic": [{
            "cure": "Copper fungicide spray.",
            "dosage": "2g/L weekly.",
            "prevention": "Improve ventilation."
        }],
        "chemical": [{
            "cure": "Metalaxyl or Mancozeb.",
            "dosage": "As per label.",
            "prevention": "Spray early."
        }],
        "weather_rules": {"heavy_rain_mm": 8, "humidity_high_pct": 90}
    },

    "tomato_leaf_mold": {
        "organic": [{
            "cure": "Baking soda spray.",
            "dosage": "5g/L water weekly.",
            "prevention": "Improve air flow."
        }],
        "chemical": [{
            "cure": "Chlorothalonil.",
            "dosage": "2g/L.",
            "prevention": "Maintain leaf dryness."
        }],
        "weather_rules": {"heavy_rain_mm": 8, "humidity_high_pct": 85}
    },

    "tomato_septoria_leaf_spot": {
        "organic": [{
            "cure": "Neem oil spray.",
            "dosage": "3ml/L weekly.",
            "prevention": "Remove leaf debris."
        }],
        "chemical": [{
            "cure": "Mancozeb.",
            "dosage": "2.5g/L.",
            "prevention": "Preventative spraying."
        }],
        "weather_rules": {"heavy_rain_mm": 10, "humidity_high_pct": 85}
    },

    "tomato_spider_mites_two_spotted_spider_mite": {
        "organic": [{
            "cure": "Neem oil or insecticidal soap.",
            "dosage": "3ml/L twice a week.",
            "prevention": "Keep humidity high."
        }],
        "chemical": [{
            "cure": "Abamectin.",
            "dosage": "As per label.",
            "prevention": "Monitor weekly."
        }],
        "weather_rules": {"heavy_rain_mm": 15, "humidity_high_pct": 70}
    },

    "tomato_target_spot": {
        "organic": [{
            "cure": "Copper spray.",
            "dosage": "2g/L weekly.",
            "prevention": "Avoid contaminated soil."
        }],
        "chemical": [{
            "cure": "Azoxystrobin.",
            "dosage": "As per instructions.",
            "prevention": "Rotate fungicides."
        }],
        "weather_rules": {"heavy_rain_mm": 10, "humidity_high_pct": 80}
    },

    "tomato_tomato_yellowleaf_curl_virus": {
        "organic": [{
            "cure": "Neem oil and remove infected plants.",
            "dosage": "3ml/L weekly.",
            "prevention": "Control whiteflies."
        }],
        "chemical": [{
            "cure": "Imidacloprid for vector control.",
            "dosage": "As per label.",
            "prevention": "Use resistant varieties."
        }],
        "weather_rules": {"heavy_rain_mm": 10, "humidity_high_pct": 80}
    },

    "tomato_tomato_mosaic_virus": {
        "organic": [{
            "cure": "Remove infected plants.",
            "dosage": "-",
            "prevention": "Sterilise tools."
        }],
        "chemical": [{
            "cure": "No chemical cure.",
            "dosage": "-",
            "prevention": "Virus-free seedlings."
        }],
        "weather_rules": {}
    },

    "tomato_healthy": {
        "organic": [{"cure": "No treatment needed.", "dosage": "-", "prevention": "Maintain plant health."}],
        "chemical": [{"cure": "-", "dosage": "-", "prevention": "-"}],
        "weather_rules": {}
    }
},

# ============================================================
# PEPPER
# ============================================================
"pepper": {

    "pepper__bell_bacterial_spot": {
        "organic": [{
            "cure": "Neem oil and garlic extract spray.",
            "dosage": "3ml/L weekly.",
            "prevention": "Avoid wet foliage."
        }],
        "chemical": [{
            "cure": "Copper fungicide.",
            "dosage": "As per label.",
            "prevention": "Clean tools regularly."
        }],
        "weather_rules": {"heavy_rain_mm": 10, "humidity_high_pct": 80}
    },

    "pepper__bell_healthy": {
        "organic": [{"cure": "No treatment required.", "dosage": "-", "prevention": "Keep monitoring."}],
        "chemical": [{"cure": "-", "dosage": "-", "prevention": "-"}],
        "weather_rules": {}
    }
},

# ============================================================
# RICE
# ============================================================
"rice": {
    "bacterial_leaf_blight": {
        "organic": [{
            "cure": "Neem extract and remove infected plants.",
            "dosage": "3ml/L water.",
            "prevention": "Use resistant varieties."
        }],
        "chemical": [{
            "cure": "Streptocycline + Copper oxychloride.",
            "dosage": "1g/10L + 3g/L.",
            "prevention": "Apply early."
        }],
        "weather_rules": {"heavy_rain_mm": 20, "humidity_high_pct": 80}
    },

    "normal": {
        "organic": [{"cure": "No treatment needed.", "dosage": "-", "prevention": "Continue monitoring."}],
        "chemical": [{"cure": "-", "dosage": "-", "prevention": "-"}],
        "weather_rules": {}
    }
}
}
