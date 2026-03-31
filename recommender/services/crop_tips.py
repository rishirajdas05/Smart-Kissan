# recommender/services/crop_tips.py

_DATA = {
    "Cotton": {
        "essentials": ["Warm climate (21–30°C)", "Low–moderate rainfall", "pH 5.5–8.0"],
        "tips": ["Avoid excess nitrogen (pest risk)", "Monitor bollworm", "Good spacing + aeration"],
    },
    "Wheat": {
        "essentials": ["Cool season crop", "pH 6.0–7.5", "Well-drained soil"],
        "tips": ["Use certified seeds", "Avoid waterlogging", "Timely irrigation at CRI stage"],
    },
}

def get_crop_tips(crop: str):
    # fallback so UI never breaks
    return _DATA.get(crop, {"essentials": ["No data yet"], "tips": ["No data yet"]})
