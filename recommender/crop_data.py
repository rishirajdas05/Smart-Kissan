# recommender/crop_data.py
# 100+ Indian crops with accurate ranges
# climate_zone: "plains", "hill", "coastal", "arid", "all"
# Hard disqualification in views.py uses climate_zone + temp ranges

CROPS = [
    # ===== Cereals =====
    {"name":"Rice","season":"Kharif","climate_zone":"all","ph_min":5.5,"ph_max":7.5,"temp_min":20,"temp_max":35,"hum_min":60,"hum_max":95,"rain_min":100,"rain_max":300,"n_need":"High"},
    {"name":"Wheat","season":"Rabi","climate_zone":"plains","ph_min":6.0,"ph_max":7.8,"temp_min":10,"temp_max":25,"hum_min":30,"hum_max":70,"rain_min":30,"rain_max":120,"n_need":"Medium"},
    {"name":"Maize","season":"Kharif","climate_zone":"all","ph_min":5.5,"ph_max":7.5,"temp_min":18,"temp_max":32,"hum_min":40,"hum_max":85,"rain_min":50,"rain_max":200,"n_need":"High"},
    {"name":"Barley","season":"Rabi","climate_zone":"plains","ph_min":6.0,"ph_max":8.0,"temp_min":12,"temp_max":25,"hum_min":30,"hum_max":70,"rain_min":20,"rain_max":100,"n_need":"Low"},
    {"name":"Sorghum (Jowar)","season":"Kharif","climate_zone":"arid","ph_min":5.5,"ph_max":8.5,"temp_min":20,"temp_max":35,"hum_min":30,"hum_max":80,"rain_min":40,"rain_max":150,"n_need":"Medium"},
    {"name":"Pearl Millet (Bajra)","season":"Kharif","climate_zone":"arid","ph_min":5.0,"ph_max":8.5,"temp_min":22,"temp_max":38,"hum_min":20,"hum_max":70,"rain_min":30,"rain_max":120,"n_need":"Low"},
    {"name":"Finger Millet (Ragi)","season":"Kharif","climate_zone":"all","ph_min":5.0,"ph_max":7.5,"temp_min":18,"temp_max":32,"hum_min":30,"hum_max":80,"rain_min":50,"rain_max":180,"n_need":"Low"},
    {"name":"Oats","season":"Rabi","climate_zone":"plains","ph_min":5.5,"ph_max":7.5,"temp_min":10,"temp_max":25,"hum_min":30,"hum_max":75,"rain_min":30,"rain_max":120,"n_need":"Medium"},

    # ===== Pulses =====
    {"name":"Chickpea (Gram)","season":"Rabi","climate_zone":"plains","ph_min":6.0,"ph_max":8.0,"temp_min":15,"temp_max":30,"hum_min":20,"hum_max":70,"rain_min":20,"rain_max":90,"n_need":"Low"},
    {"name":"Pigeon Pea (Arhar/Tur)","season":"Kharif","climate_zone":"plains","ph_min":5.0,"ph_max":8.0,"temp_min":18,"temp_max":35,"hum_min":40,"hum_max":85,"rain_min":60,"rain_max":200,"n_need":"Low"},
    {"name":"Green Gram (Moong)","season":"Kharif","climate_zone":"plains","ph_min":6.0,"ph_max":7.5,"temp_min":20,"temp_max":35,"hum_min":30,"hum_max":80,"rain_min":40,"rain_max":150,"n_need":"Low"},
    {"name":"Black Gram (Urad)","season":"Kharif","climate_zone":"plains","ph_min":6.0,"ph_max":7.5,"temp_min":20,"temp_max":35,"hum_min":40,"hum_max":85,"rain_min":50,"rain_max":180,"n_need":"Low"},
    {"name":"Lentil (Masoor)","season":"Rabi","climate_zone":"plains","ph_min":6.0,"ph_max":8.0,"temp_min":10,"temp_max":25,"hum_min":20,"hum_max":70,"rain_min":20,"rain_max":80,"n_need":"Low"},
    {"name":"Pea","season":"Rabi","climate_zone":"plains","ph_min":6.0,"ph_max":7.5,"temp_min":10,"temp_max":22,"hum_min":30,"hum_max":80,"rain_min":30,"rain_max":120,"n_need":"Low"},
    {"name":"Kidney Bean (Rajma)","season":"Kharif","climate_zone":"hill","ph_min":5.5,"ph_max":7.5,"temp_min":15,"temp_max":25,"hum_min":40,"hum_max":85,"rain_min":60,"rain_max":180,"n_need":"Low"},

    # ===== Oilseeds =====
    {"name":"Mustard","season":"Rabi","climate_zone":"plains","ph_min":5.5,"ph_max":8.0,"temp_min":10,"temp_max":25,"hum_min":20,"hum_max":70,"rain_min":20,"rain_max":90,"n_need":"Medium"},
    {"name":"Groundnut (Peanut)","season":"Kharif","climate_zone":"plains","ph_min":5.5,"ph_max":7.5,"temp_min":20,"temp_max":35,"hum_min":30,"hum_max":80,"rain_min":50,"rain_max":200,"n_need":"Medium"},
    {"name":"Soybean","season":"Kharif","climate_zone":"plains","ph_min":6.0,"ph_max":7.5,"temp_min":18,"temp_max":32,"hum_min":40,"hum_max":85,"rain_min":60,"rain_max":200,"n_need":"Medium"},
    {"name":"Sesame (Til)","season":"Kharif","climate_zone":"arid","ph_min":5.5,"ph_max":8.0,"temp_min":20,"temp_max":35,"hum_min":20,"hum_max":70,"rain_min":30,"rain_max":120,"n_need":"Low"},
    {"name":"Sunflower","season":"Rabi","climate_zone":"plains","ph_min":6.0,"ph_max":8.0,"temp_min":18,"temp_max":32,"hum_min":20,"hum_max":70,"rain_min":30,"rain_max":120,"n_need":"Medium"},
    {"name":"Safflower","season":"Rabi","climate_zone":"arid","ph_min":5.5,"ph_max":8.0,"temp_min":15,"temp_max":28,"hum_min":20,"hum_max":60,"rain_min":20,"rain_max":90,"n_need":"Low"},
    {"name":"Linseed (Flax)","season":"Rabi","climate_zone":"plains","ph_min":6.0,"ph_max":7.5,"temp_min":10,"temp_max":25,"hum_min":20,"hum_max":70,"rain_min":20,"rain_max":80,"n_need":"Low"},
    {"name":"Castor","season":"Kharif","climate_zone":"arid","ph_min":6.0,"ph_max":8.0,"temp_min":20,"temp_max":35,"hum_min":20,"hum_max":80,"rain_min":40,"rain_max":160,"n_need":"Low"},

    # ===== Commercial =====
    {"name":"Sugarcane","season":"Annual","climate_zone":"plains","ph_min":6.0,"ph_max":7.8,"temp_min":20,"temp_max":35,"hum_min":40,"hum_max":90,"rain_min":80,"rain_max":250,"n_need":"High"},
    {"name":"Cotton","season":"Kharif","climate_zone":"plains","ph_min":5.5,"ph_max":8.0,"temp_min":21,"temp_max":35,"hum_min":30,"hum_max":80,"rain_min":50,"rain_max":200,"n_need":"High"},
    {"name":"Jute","season":"Kharif","climate_zone":"coastal","ph_min":6.0,"ph_max":7.5,"temp_min":24,"temp_max":35,"hum_min":60,"hum_max":95,"rain_min":150,"rain_max":300,"n_need":"Medium"},

    # ===== Vegetables =====
    {"name":"Tomato","season":"All","climate_zone":"all","ph_min":5.5,"ph_max":7.5,"temp_min":18,"temp_max":32,"hum_min":30,"hum_max":85,"rain_min":40,"rain_max":160,"n_need":"High"},
    {"name":"Potato","season":"Rabi","climate_zone":"plains","ph_min":5.0,"ph_max":7.0,"temp_min":10,"temp_max":25,"hum_min":40,"hum_max":90,"rain_min":30,"rain_max":120,"n_need":"High"},
    {"name":"Onion","season":"Rabi","climate_zone":"plains","ph_min":6.0,"ph_max":7.5,"temp_min":12,"temp_max":30,"hum_min":30,"hum_max":80,"rain_min":20,"rain_max":120,"n_need":"Medium"},
    {"name":"Garlic","season":"Rabi","climate_zone":"plains","ph_min":6.0,"ph_max":7.5,"temp_min":10,"temp_max":25,"hum_min":30,"hum_max":80,"rain_min":20,"rain_max":100,"n_need":"Medium"},
    {"name":"Brinjal (Eggplant)","season":"Kharif","climate_zone":"plains","ph_min":5.5,"ph_max":7.5,"temp_min":20,"temp_max":35,"hum_min":40,"hum_max":90,"rain_min":50,"rain_max":180,"n_need":"High"},
    {"name":"Okra (Bhindi)","season":"Kharif","climate_zone":"plains","ph_min":6.0,"ph_max":7.5,"temp_min":20,"temp_max":35,"hum_min":30,"hum_max":85,"rain_min":40,"rain_max":160,"n_need":"Medium"},
    {"name":"Cauliflower","season":"Rabi","climate_zone":"plains","ph_min":6.0,"ph_max":7.5,"temp_min":10,"temp_max":25,"hum_min":40,"hum_max":90,"rain_min":30,"rain_max":120,"n_need":"High"},
    {"name":"Cabbage","season":"Rabi","climate_zone":"plains","ph_min":6.0,"ph_max":7.5,"temp_min":10,"temp_max":25,"hum_min":40,"hum_max":90,"rain_min":30,"rain_max":120,"n_need":"High"},
    {"name":"Chilli","season":"Kharif","climate_zone":"plains","ph_min":6.0,"ph_max":7.5,"temp_min":18,"temp_max":32,"hum_min":30,"hum_max":85,"rain_min":40,"rain_max":160,"n_need":"Medium"},
    {"name":"Capsicum","season":"All","climate_zone":"all","ph_min":6.0,"ph_max":7.0,"temp_min":18,"temp_max":30,"hum_min":40,"hum_max":85,"rain_min":40,"rain_max":160,"n_need":"Medium"},
    {"name":"Cucumber","season":"Kharif","climate_zone":"plains","ph_min":5.5,"ph_max":7.5,"temp_min":18,"temp_max":32,"hum_min":40,"hum_max":90,"rain_min":40,"rain_max":180,"n_need":"Medium"},
    {"name":"Pumpkin","season":"Kharif","climate_zone":"plains","ph_min":5.5,"ph_max":7.5,"temp_min":18,"temp_max":35,"hum_min":40,"hum_max":90,"rain_min":40,"rain_max":200,"n_need":"Medium"},
    {"name":"Bottle Gourd (Lauki)","season":"Kharif","climate_zone":"plains","ph_min":6.0,"ph_max":7.5,"temp_min":18,"temp_max":35,"hum_min":40,"hum_max":90,"rain_min":40,"rain_max":180,"n_need":"Medium"},
    {"name":"Bitter Gourd (Karela)","season":"Kharif","climate_zone":"plains","ph_min":6.0,"ph_max":7.5,"temp_min":20,"temp_max":35,"hum_min":40,"hum_max":90,"rain_min":40,"rain_max":180,"n_need":"Medium"},
    {"name":"Ridge Gourd (Turai)","season":"Kharif","climate_zone":"plains","ph_min":6.0,"ph_max":7.5,"temp_min":20,"temp_max":35,"hum_min":40,"hum_max":90,"rain_min":40,"rain_max":180,"n_need":"Medium"},
    {"name":"Spinach","season":"Rabi","climate_zone":"plains","ph_min":6.0,"ph_max":7.5,"temp_min":10,"temp_max":25,"hum_min":40,"hum_max":90,"rain_min":20,"rain_max":120,"n_need":"Medium"},
    {"name":"Carrot","season":"Rabi","climate_zone":"plains","ph_min":6.0,"ph_max":7.0,"temp_min":10,"temp_max":25,"hum_min":40,"hum_max":85,"rain_min":20,"rain_max":120,"n_need":"Low"},
    {"name":"Radish","season":"Rabi","climate_zone":"plains","ph_min":5.5,"ph_max":7.5,"temp_min":10,"temp_max":25,"hum_min":40,"hum_max":85,"rain_min":20,"rain_max":120,"n_need":"Low"},
    {"name":"Beetroot","season":"Rabi","climate_zone":"plains","ph_min":6.0,"ph_max":7.5,"temp_min":10,"temp_max":25,"hum_min":40,"hum_max":85,"rain_min":20,"rain_max":120,"n_need":"Low"},

    # ===== Fruits (plains/tropical) =====
    {"name":"Mango","season":"Annual","climate_zone":"plains","ph_min":5.5,"ph_max":7.5,"temp_min":20,"temp_max":40,"hum_min":40,"hum_max":85,"rain_min":50,"rain_max":250,"n_need":"Medium"},
    {"name":"Banana","season":"Annual","climate_zone":"coastal","ph_min":6.0,"ph_max":7.5,"temp_min":20,"temp_max":35,"hum_min":50,"hum_max":95,"rain_min":100,"rain_max":250,"n_need":"High"},
    {"name":"Guava","season":"Annual","climate_zone":"plains","ph_min":5.5,"ph_max":7.5,"temp_min":15,"temp_max":35,"hum_min":30,"hum_max":85,"rain_min":40,"rain_max":200,"n_need":"Medium"},
    {"name":"Papaya","season":"Annual","climate_zone":"plains","ph_min":6.0,"ph_max":7.0,"temp_min":20,"temp_max":35,"hum_min":40,"hum_max":85,"rain_min":60,"rain_max":200,"n_need":"High"},
    {"name":"Orange","season":"Annual","climate_zone":"plains","ph_min":5.5,"ph_max":7.5,"temp_min":15,"temp_max":32,"hum_min":40,"hum_max":85,"rain_min":60,"rain_max":200,"n_need":"Medium"},
    {"name":"Lemon","season":"Annual","climate_zone":"plains","ph_min":5.5,"ph_max":7.5,"temp_min":15,"temp_max":35,"hum_min":40,"hum_max":85,"rain_min":60,"rain_max":200,"n_need":"Medium"},
    {"name":"Pomegranate","season":"Annual","climate_zone":"arid","ph_min":6.0,"ph_max":8.0,"temp_min":18,"temp_max":38,"hum_min":20,"hum_max":70,"rain_min":20,"rain_max":120,"n_need":"Low"},
    {"name":"Grapes","season":"Annual","climate_zone":"arid","ph_min":6.0,"ph_max":7.5,"temp_min":18,"temp_max":38,"hum_min":20,"hum_max":70,"rain_min":20,"rain_max":120,"n_need":"Medium"},
    {"name":"Watermelon","season":"Kharif","climate_zone":"arid","ph_min":6.0,"ph_max":7.5,"temp_min":22,"temp_max":38,"hum_min":30,"hum_max":80,"rain_min":30,"rain_max":150,"n_need":"Medium"},
    {"name":"Muskmelon","season":"Kharif","climate_zone":"arid","ph_min":6.0,"ph_max":7.5,"temp_min":22,"temp_max":38,"hum_min":30,"hum_max":80,"rain_min":30,"rain_max":150,"n_need":"Medium"},
    {"name":"Pineapple","season":"Annual","climate_zone":"coastal","ph_min":5.0,"ph_max":6.5,"temp_min":22,"temp_max":32,"hum_min":60,"hum_max":95,"rain_min":100,"rain_max":250,"n_need":"Medium"},
    {"name":"Coconut","season":"Annual","climate_zone":"coastal","ph_min":5.5,"ph_max":8.0,"temp_min":22,"temp_max":35,"hum_min":60,"hum_max":95,"rain_min":100,"rain_max":300,"n_need":"Medium"},
    {"name":"Jackfruit","season":"Annual","climate_zone":"coastal","ph_min":6.0,"ph_max":7.5,"temp_min":22,"temp_max":35,"hum_min":60,"hum_max":95,"rain_min":100,"rain_max":250,"n_need":"Low"},
    {"name":"Litchi","season":"Annual","climate_zone":"plains","ph_min":5.5,"ph_max":7.0,"temp_min":18,"temp_max":32,"hum_min":50,"hum_max":90,"rain_min":80,"rain_max":200,"n_need":"Medium"},
    {"name":"Amla","season":"Annual","climate_zone":"plains","ph_min":5.0,"ph_max":8.0,"temp_min":15,"temp_max":35,"hum_min":30,"hum_max":85,"rain_min":40,"rain_max":200,"n_need":"Low"},
    {"name":"Ber (Jujube)","season":"Annual","climate_zone":"arid","ph_min":6.0,"ph_max":8.0,"temp_min":18,"temp_max":42,"hum_min":15,"hum_max":75,"rain_min":15,"rain_max":150,"n_need":"Low"},
    {"name":"Kinnow","season":"Annual","climate_zone":"plains","ph_min":6.0,"ph_max":7.5,"temp_min":15,"temp_max":32,"hum_min":40,"hum_max":85,"rain_min":50,"rain_max":180,"n_need":"Medium"},
    {"name":"Mosambi","season":"Annual","climate_zone":"plains","ph_min":6.0,"ph_max":7.5,"temp_min":18,"temp_max":32,"hum_min":40,"hum_max":85,"rain_min":60,"rain_max":180,"n_need":"Medium"},

    # ===== HILL FRUITS — corrected temp ranges =====
    # Apple: strictly cool climate, needs chill hours (1000+ hrs below 7°C)
    {"name":"Apple","season":"Annual","climate_zone":"hill","ph_min":5.5,"ph_max":7.0,"temp_min":7,"temp_max":18,"hum_min":60,"hum_max":90,"rain_min":100,"rain_max":200,"n_need":"Medium"},
    # Pear: similar to apple, cool temperate
    {"name":"Pear","season":"Annual","climate_zone":"hill","ph_min":6.0,"ph_max":7.5,"temp_min":7,"temp_max":20,"hum_min":60,"hum_max":90,"rain_min":80,"rain_max":180,"n_need":"Medium"},
    # Peach: cool climate, needs chilling
    {"name":"Peach","season":"Annual","climate_zone":"hill","ph_min":6.0,"ph_max":7.5,"temp_min":8,"temp_max":22,"hum_min":50,"hum_max":85,"rain_min":70,"rain_max":180,"n_need":"Medium"},
    # Plum: temperate hill fruit
    {"name":"Plum","season":"Annual","climate_zone":"hill","ph_min":5.5,"ph_max":7.5,"temp_min":8,"temp_max":22,"hum_min":50,"hum_max":85,"rain_min":70,"rain_max":180,"n_need":"Medium"},
    # Apricot: very cold tolerant
    {"name":"Apricot","season":"Annual","climate_zone":"hill","ph_min":6.0,"ph_max":7.5,"temp_min":5,"temp_max":18,"hum_min":40,"hum_max":80,"rain_min":50,"rain_max":150,"n_need":"Low"},
    # Walnut: high altitude
    {"name":"Walnut","season":"Annual","climate_zone":"hill","ph_min":6.0,"ph_max":7.5,"temp_min":5,"temp_max":20,"hum_min":50,"hum_max":85,"rain_min":80,"rain_max":200,"n_need":"Low"},
    # Cherry: cool hill climate
    {"name":"Cherry","season":"Annual","climate_zone":"hill","ph_min":6.0,"ph_max":7.5,"temp_min":5,"temp_max":18,"hum_min":55,"hum_max":85,"rain_min":80,"rain_max":180,"n_need":"Low"},

    # ===== Spices / Plantation =====
    {"name":"Turmeric","season":"Kharif","climate_zone":"coastal","ph_min":5.5,"ph_max":7.5,"temp_min":20,"temp_max":35,"hum_min":60,"hum_max":95,"rain_min":120,"rain_max":250,"n_need":"Medium"},
    {"name":"Ginger","season":"Kharif","climate_zone":"coastal","ph_min":5.5,"ph_max":7.0,"temp_min":20,"temp_max":35,"hum_min":60,"hum_max":95,"rain_min":120,"rain_max":250,"n_need":"Medium"},
    {"name":"Coriander","season":"Rabi","climate_zone":"plains","ph_min":6.0,"ph_max":8.0,"temp_min":10,"temp_max":25,"hum_min":30,"hum_max":75,"rain_min":20,"rain_max":90,"n_need":"Low"},
    {"name":"Cumin","season":"Rabi","climate_zone":"arid","ph_min":6.5,"ph_max":8.0,"temp_min":10,"temp_max":25,"hum_min":20,"hum_max":60,"rain_min":10,"rain_max":60,"n_need":"Low"},
    {"name":"Tea","season":"Annual","climate_zone":"hill","ph_min":4.5,"ph_max":6.0,"temp_min":13,"temp_max":28,"hum_min":60,"hum_max":95,"rain_min":150,"rain_max":300,"n_need":"Medium"},
    {"name":"Coffee","season":"Annual","climate_zone":"coastal","ph_min":5.0,"ph_max":6.5,"temp_min":15,"temp_max":28,"hum_min":60,"hum_max":95,"rain_min":150,"rain_max":300,"n_need":"Medium"},
    {"name":"Cardamom","season":"Annual","climate_zone":"hill","ph_min":5.0,"ph_max":6.5,"temp_min":15,"temp_max":25,"hum_min":70,"hum_max":95,"rain_min":200,"rain_max":400,"n_need":"Medium"},
    {"name":"Black Pepper","season":"Annual","climate_zone":"coastal","ph_min":5.0,"ph_max":7.0,"temp_min":20,"temp_max":35,"hum_min":60,"hum_max":95,"rain_min":150,"rain_max":300,"n_need":"Medium"},
    {"name":"Saffron","season":"Annual","climate_zone":"hill","ph_min":6.0,"ph_max":8.0,"temp_min":5,"temp_max":20,"hum_min":30,"hum_max":70,"rain_min":30,"rain_max":100,"n_need":"Low"},

    # ===== Millets =====
    {"name":"Kodo Millet","season":"Kharif","climate_zone":"plains","ph_min":5.0,"ph_max":8.0,"temp_min":20,"temp_max":35,"hum_min":30,"hum_max":80,"rain_min":40,"rain_max":150,"n_need":"Low"},
    {"name":"Foxtail Millet","season":"Kharif","climate_zone":"plains","ph_min":5.5,"ph_max":7.5,"temp_min":20,"temp_max":35,"hum_min":30,"hum_max":80,"rain_min":30,"rain_max":120,"n_need":"Low"},
    {"name":"Barnyard Millet","season":"Kharif","climate_zone":"hill","ph_min":5.0,"ph_max":7.5,"temp_min":15,"temp_max":30,"hum_min":30,"hum_max":80,"rain_min":40,"rain_max":150,"n_need":"Low"},

    # ===== Fodder / Others =====
    {"name":"Sweet Potato","season":"Kharif","climate_zone":"plains","ph_min":5.5,"ph_max":7.5,"temp_min":20,"temp_max":35,"hum_min":40,"hum_max":90,"rain_min":50,"rain_max":200,"n_need":"Medium"},
    {"name":"Tapioca","season":"Annual","climate_zone":"coastal","ph_min":5.5,"ph_max":7.5,"temp_min":22,"temp_max":35,"hum_min":50,"hum_max":95,"rain_min":100,"rain_max":250,"n_need":"Medium"},
    {"name":"French Bean","season":"All","climate_zone":"all","ph_min":6.0,"ph_max":7.5,"temp_min":15,"temp_max":28,"hum_min":40,"hum_max":85,"rain_min":40,"rain_max":150,"n_need":"Low"},
    {"name":"Cowpea","season":"Kharif","climate_zone":"arid","ph_min":6.0,"ph_max":8.0,"temp_min":22,"temp_max":38,"hum_min":30,"hum_max":80,"rain_min":30,"rain_max":150,"n_need":"Low"},
    {"name":"Drumstick","season":"Annual","climate_zone":"arid","ph_min":6.0,"ph_max":8.0,"temp_min":20,"temp_max":40,"hum_min":20,"hum_max":80,"rain_min":25,"rain_max":150,"n_need":"Low"},
    {"name":"Broccoli","season":"Rabi","climate_zone":"plains","ph_min":6.0,"ph_max":7.0,"temp_min":10,"temp_max":22,"hum_min":40,"hum_max":90,"rain_min":30,"rain_max":120,"n_need":"High"},
    {"name":"Fenugreek","season":"Rabi","climate_zone":"plains","ph_min":6.0,"ph_max":8.0,"temp_min":10,"temp_max":28,"hum_min":30,"hum_max":80,"rain_min":20,"rain_max":100,"n_need":"Low"},
    {"name":"Mint","season":"All","climate_zone":"plains","ph_min":6.0,"ph_max":7.5,"temp_min":15,"temp_max":30,"hum_min":40,"hum_max":90,"rain_min":40,"rain_max":150,"n_need":"Medium"},
    {"name":"Aloe Vera","season":"Annual","climate_zone":"arid","ph_min":6.0,"ph_max":8.0,"temp_min":15,"temp_max":40,"hum_min":10,"hum_max":70,"rain_min":10,"rain_max":100,"n_need":"Low"},
    {"name":"Ashwagandha","season":"Kharif","climate_zone":"arid","ph_min":7.5,"ph_max":8.0,"temp_min":20,"temp_max":38,"hum_min":20,"hum_max":70,"rain_min":20,"rain_max":100,"n_need":"Low"},
    {"name":"Moringa","season":"Annual","climate_zone":"arid","ph_min":6.0,"ph_max":8.0,"temp_min":20,"temp_max":40,"hum_min":20,"hum_max":80,"rain_min":25,"rain_max":150,"n_need":"Low"},
    {"name":"Stevia","season":"Annual","climate_zone":"plains","ph_min":6.5,"ph_max":7.5,"temp_min":15,"temp_max":30,"hum_min":40,"hum_max":85,"rain_min":40,"rain_max":150,"n_need":"Medium"},
    {"name":"Marigold","season":"All","climate_zone":"all","ph_min":6.0,"ph_max":7.5,"temp_min":15,"temp_max":30,"hum_min":40,"hum_max":85,"rain_min":30,"rain_max":150,"n_need":"Medium"},
    {"name":"Rose","season":"All","climate_zone":"plains","ph_min":6.0,"ph_max":7.0,"temp_min":15,"temp_max":28,"hum_min":40,"hum_max":85,"rain_min":40,"rain_max":150,"n_need":"Medium"},
    {"name":"Arecanut","season":"Annual","climate_zone":"coastal","ph_min":6.0,"ph_max":7.5,"temp_min":22,"temp_max":35,"hum_min":60,"hum_max":95,"rain_min":150,"rain_max":350,"n_need":"Medium"},
    {"name":"Rubber","season":"Annual","climate_zone":"coastal","ph_min":4.5,"ph_max":6.5,"temp_min":22,"temp_max":32,"hum_min":70,"hum_max":95,"rain_min":200,"rain_max":400,"n_need":"Medium"},
    {"name":"Bamboo","season":"Annual","climate_zone":"all","ph_min":5.5,"ph_max":7.5,"temp_min":15,"temp_max":35,"hum_min":40,"hum_max":95,"rain_min":80,"rain_max":300,"n_need":"Low"},
    {"name":"Isabgol","season":"Rabi","climate_zone":"arid","ph_min":7.0,"ph_max":8.5,"temp_min":10,"temp_max":25,"hum_min":20,"hum_max":60,"rain_min":10,"rain_max":60,"n_need":"Low"},
    {"name":"Sugar Beet","season":"Rabi","climate_zone":"plains","ph_min":6.0,"ph_max":8.0,"temp_min":10,"temp_max":25,"hum_min":30,"hum_max":80,"rain_min":30,"rain_max":120,"n_need":"Medium"},
    {"name":"Guar","season":"Kharif","climate_zone":"arid","ph_min":7.0,"ph_max":8.5,"temp_min":25,"temp_max":40,"hum_min":15,"hum_max":60,"rain_min":20,"rain_max":100,"n_need":"Low"},
    {"name":"Lucerne","season":"Annual","climate_zone":"plains","ph_min":6.5,"ph_max":8.0,"temp_min":15,"temp_max":32,"hum_min":30,"hum_max":80,"rain_min":40,"rain_max":180,"n_need":"Medium"},
]