treatments = {

    # ==============================
    # POTATO
    # ==============================
    "potato": {
        "early_blight": {
            "organic": [{
                "cure": "Neem oil spray, Bacillus subtilis products, or botanicals like garlic extract.",
                "dosage": "Neem oil: 2-4 ml per liter, weekly.",
                "prevention": "Rotate crops, remove infected foliage, avoid overhead irrigation."
            }],
            "chemical": [{
                "cure": "Chlorothalonil, Mancozeb, Azoxystrobin combinations.",
                "dosage": "Chlorothalonil: 2g/L; Mancozeb: 2.5g/L.",
                "prevention": "Apply preventatively during warm/humid periods."
            }],
            "weather_rules": {
                "heavy_rain_mm": 10,
                "humidity_high_pct": 85
            }
        },

        "late_blight": {
            "organic": [{
                "cure": "Copper fungicides or compost tea.",
                "dosage": "Copper oxychloride: 0.9 lbs elemental copper/acre.",
                "prevention": "Plant resistant varieties; improve airflow."
            }],
            "chemical": [{
                "cure": "Mancozeb, Chlorothalonil.",
                "dosage": "Mancozeb: 2.5g/L every 10–14 days.",
                "prevention": "Maintain regular spray intervals."
            }],
            "weather_rules": {
                "heavy_rain_mm": 8,
                "humidity_high_pct": 90
            }
        },

        "healthy": {
            "organic": [{"cure": "No treatment needed.", "dosage": "-", "prevention": "Maintain monitoring."}],
            "chemical": [{"cure": "-", "dosage": "-", "prevention": "-"}],
            "weather_rules": {}
        }
    },

    # ==============================
    # TOMATO (placeholder)
    # ==============================
    "tomato": {
        "tomato_bacterial_spot": { ... },
        "tomato_early_blight": { ... },
        "tomato_late_blight": { ... },
        "tomato_leaf_mold": { ... },
        "tomato_septoria_leaf_spot": { ... },
        "tomato_spider_mites_two_spotted_spider_mite": { ... },
        "tomato_target_spot": { ... },
        "tomato_tomato_yellowleaf_curl_virus": { ... },
        "tomato_tomato_mosaic_virus": { ... },
        "tomato_healthy": { ... }
    },

    # ==============================
    # PEPPER
    # ==============================
    "pepper": {
        "pepper__bell_bacterial_spot": { ... },
        "pepper__bell_healthy": { ... }
    },

    # ==============================
    # RICE (weather-aware)
    # ==============================
    "rice": {
        "bacterial_leaf_blight": {
            "organic": [{
                "cure": "Improve drainage, remove infected plants, apply neem extract.",
                "dosage": "Neem extract: 3ml/L.",
                "prevention": "Use resistant varieties; avoid stagnant water."
            }],
            "chemical": [{
                "cure": "Streptocycline + Copper oxychloride",
                "dosage": "Streptocycline: 1g/10L; Copper oxychloride: 3g/L.",
                "prevention": "Apply at first symptoms; maintain field sanitation."
            }],
            "weather_rules": {
                "heavy_rain_mm": 20,
                "humidity_high_pct": 80
            }
        },

        "bacterial_leaf_streak": {
            "organic": [{
                "cure": "Use disease-free seeds, field sanitation.",
                "dosage": "-",
                "prevention": "Keep nitrogen under recommended levels."
            }],
            "chemical": [{
                "cure": "Copper fungicides.",
                "dosage": "Follow label.",
                "prevention": "Alternate fungicides to avoid resistance."
            }],
            "weather_rules": {
                "heavy_rain_mm": 15,
                "humidity_high_pct": 85
            }
        },

        "bacterial_panicle_blight": {
            "organic": [{
                "cure": "Improve field drainage and fertilizer balance.",
                "dosage": "-",
                "prevention": "Avoid excessive nitrogen."
            }],
            "chemical": [{
                "cure": "No fully effective chemical cure.",
                "dosage": "-",
                "prevention": "Use resistant varieties."
            }],
            "weather_rules": {
                "heavy_rain_mm": 12,
                "humidity_high_pct": 85
            }
        },

        "blast": {
            "organic": [{
                "cure": "Maintain flooding until booting stage.",
                "dosage": "-",
                "prevention": "Use silicon fertilizers."
            }],
            "chemical": [{
                "cure": "Tricyclazole or Isoprothiolane.",
                "dosage": "Tricyclazole: 0.6g/L.",
                "prevention": "Spray at first signs."
            }],
            "weather_rules": {
                "heavy_rain_mm": 8,
                "humidity_high_pct": 90
            }
        },

        "brown_spot": {
            "organic": [{
                "cure": "Apply farmyard manure and compost.",
                "dosage": "-",
                "prevention": "Avoid nutrient deficiency."
            }],
            "chemical": [{
                "cure": "Propiconazole or Mancozeb.",
                "dosage": "As per label.",
                "prevention": "Repeat in 10-day intervals."
            }],
            "weather_rules": {
                "heavy_rain_mm": 10,
                "humidity_high_pct": 85
            }
        },

        "dead_heart": {
            "organic": [{
                "cure": "Use neem-based sprays.",
                "dosage": "Neem oil: 3ml/L.",
                "prevention": "Encourage natural predators."
            }],
            "chemical": [{
                "cure": "Chlorpyrifos (for larvae).",
                "dosage": "As per label.",
                "prevention": "Apply when threshold exceeds limits."
            }],
            "weather_rules": {
                "heavy_rain_mm": 20,
                "humidity_high_pct": 75
            }
        },

        "downy_mildew": {
            "organic": [{
                "cure": "Improve aeration and drainage.",
                "dosage": "-",
                "prevention": "Avoid overcrowding."
            }],
            "chemical": [{
                "cure": "Metalaxyl + Mancozeb.",
                "dosage": "As per label.",
                "prevention": "Spray early in disease cycle."
            }],
            "weather_rules": {
                "heavy_rain_mm": 12,
                "humidity_high_pct": 80
            }
        },

        "hispa": {
            "organic": [{
                "cure": "Hand-pick larvae, apply neem extracts.",
                "dosage": "-",
                "prevention": "Encourage parasitoids."
            }],
            "chemical": [{
                "cure": "Lambda-cyhalothrin.",
                "dosage": "As per label.",
                "prevention": "Monitor larvae regularly."
            }],
            "weather_rules": {
                "heavy_rain_mm": 18,
                "humidity_high_pct": 75
            }
        },

        "normal": {
            "organic": [{"cure": "No treatment needed.", "dosage": "-", "prevention": "Continue monitoring."}],
            "chemical": [{"cure": "-", "dosage": "-", "prevention": "-"}],
            "weather_rules": {}
        },

        "tungro": {
            "organic": [{
                "cure": "Remove infected plants; use resistant varieties.",
                "dosage": "-",
                "prevention": "Control green leaf hopper vector."
            }],
            "chemical": [{
                "cure": "Imidacloprid for vector control.",
                "dosage": "Follow label.",
                "prevention": "Plant early to avoid vector build up."
            }],
            "weather_rules": {
                "heavy_rain_mm": 10,
                "humidity_high_pct": 80
            }
        }
    }
}
