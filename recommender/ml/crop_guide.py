_GUIDE = {
    "rice": {
        "essentials": ["Clay/loamy soil", "High water availability", "Warm temperature (20–35°C)"],
        "tips": ["Keep field flooded in early growth", "Use nitrogen in split doses", "Control weeds early"],
    },
    "maize": {
        "essentials": ["Well-drained soil", "Moderate rainfall", "Full sunlight"],
        "tips": ["Avoid waterlogging", "Top-dress nitrogen at knee-high stage", "Maintain spacing for airflow"],
    },
    "coffee": {
        "essentials": ["Shade & cool climate", "Well-drained soil", "Regular moisture"],
        "tips": ["Use mulching to retain moisture", "Prune for healthy branches", "Control pests (borer) regularly"],
    },
    "cotton": {
        "essentials": ["Warm climate", "Deep soil", "Moderate rainfall"],
        "tips": ["Avoid excess nitrogen (too much vegetative growth)", "Watch for bollworm", "Ensure good drainage"],
    },
    "banana": {
        "essentials": ["Rich organic soil", "Frequent irrigation", "Wind protection"],
        "tips": ["Use mulch + compost", "Support plants during fruiting", "Remove suckers properly"],
    },
    "apple": {
        "essentials": ["Cool climate", "Well-drained loamy soil", "Good chilling hours"],
        "tips": ["Prune in dormancy", "Prevent fungal diseases", "Use balanced NPK + micronutrients"],
    },
    "mango": {
        "essentials": ["Warm climate", "Well-drained soil", "Dry period for flowering"],
        "tips": ["Avoid over-irrigation during flowering", "Control fruit fly", "Use potash for fruit quality"],
    },
    "grapes": {
        "essentials": ["Dry sunny climate", "Trellis support", "Well-drained soil"],
        "tips": ["Prune for better yield", "Drip irrigation preferred", "Use sulphur spray if needed"],
    },
    "orange": {
        "essentials": ["Warm climate", "Sandy loam soil", "Regular irrigation"],
        "tips": ["Avoid water stress during fruit set", "Use organic manure yearly", "Control leaf miner"],
    },
    "watermelon": {
        "essentials": ["Sandy soil", "Hot climate", "Low humidity"],
        "tips": ["Avoid standing water", "Pollination improves fruit set", "Use mulch to reduce weeds"],
    },
    "papaya": {
        "essentials": ["Warm climate", "Well-drained soil", "Consistent moisture"],
        "tips": ["Avoid strong winds", "Keep pH around 6–7", "Use compost + potash for fruit"],
    },
    "pomegranate": {
        "essentials": ["Dry climate", "Well-drained soil", "Moderate irrigation"],
        "tips": ["Avoid humidity (fungal issues)", "Use drip irrigation", "Prune to open canopy"],
    },
}


def get_crop_guide(crop: str) -> dict:
    crop = (crop or "").lower().strip()
    data = _GUIDE.get(crop)
    if data:
        return data
    return {
        "essentials": ["Well-drained soil", "Balanced NPK", "Adequate irrigation"],
        "tips": ["Test soil before sowing", "Use organic compost", "Monitor pests regularly"],
    }
