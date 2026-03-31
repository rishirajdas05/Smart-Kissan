CROP_INFO = {
    "rice": {
        "tips": ["Keep standing water in early stage", "Use good drainage at maturity", "Weed control is critical"],
        "essentials": ["Warm climate", "High rainfall/irrigation", "Nitrogen split dose"],
    },
    "maize": {
        "tips": ["Avoid waterlogging", "Apply N in splits", "Scout for fall armyworm"],
        "essentials": ["Moderate rainfall", "Well-drained soil", "Balanced NPK"],
    },
    "wheat": {
        "tips": ["Irrigate at crown root initiation", "Avoid lodging", "Use timely sowing"],
        "essentials": ["Cool season", "Good soil moisture", "Nitrogen + phosphorus"],
    },
    "coffee": {
        "tips": ["Provide shade regulation", "Mulch for moisture", "Prune to improve yield"],
        "essentials": ["Humid climate", "Well-drained soil", "Organic matter rich"],
    },
}

def get_crop_info(name: str) -> dict:
    key = (name or "").strip().lower()
    data = CROP_INFO.get(key)
    if data:
        return data
    return {
        "tips": ["Maintain balanced NPK", "Follow proper irrigation schedule", "Monitor pests regularly"],
        "essentials": ["Healthy soil", "Water availability", "Climate suitability"],
    }
