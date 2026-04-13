import requests
from django.conf import settings


def get_weather(city):
    api_key = getattr(settings, 'OPENWEATHER_API_KEY', '')
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"
        r = requests.get(url, timeout=6)
        if r.status_code == 200:
            d = r.json()
            return {
                'city': d['name'],
                'temp': round(d['main']['temp'], 1),
                'humidity': d['main']['humidity'],
                'description': d['weather'][0]['description'].title(),
                'icon': d['weather'][0]['icon'],
                'wind': round(d['wind']['speed'] * 3.6, 1),
                'pressure': d['main']['pressure'],
                'feels_like': round(d['main']['feels_like'], 1),
                'rainfall': d.get('rain', {}).get('1h', 0),
                'success': True,
                'demo': False
            }
        else:
            return _mock_weather(city)
    except Exception:
        return _mock_weather(city)


def _mock_weather(city):
    import hashlib
    h = int(hashlib.md5(city.encode()).hexdigest(), 16) % 100
    city_weather = {
        # MP / Central India
        'indore':      {'temp': 32, 'humidity': 55, 'desc': 'Partly Cloudy',    'rain': 45},
        'bhopal':      {'temp': 30, 'humidity': 60, 'desc': 'Scattered Clouds', 'rain': 50},
        'jabalpur':    {'temp': 29, 'humidity': 65, 'desc': 'Humid',            'rain': 80},
        'gwalior':     {'temp': 35, 'humidity': 38, 'desc': 'Hot and Dry',      'rain': 25},
        'ujjain':      {'temp': 33, 'humidity': 48, 'desc': 'Sunny',            'rain': 40},
        # Maharashtra
        'mumbai':      {'temp': 28, 'humidity': 88, 'desc': 'Humid and Cloudy', 'rain': 200},
        'pune':        {'temp': 27, 'humidity': 65, 'desc': 'Pleasant',         'rain': 80},
        'nagpur':      {'temp': 33, 'humidity': 50, 'desc': 'Clear Sky',        'rain': 35},
        'nashik':      {'temp': 26, 'humidity': 60, 'desc': 'Partly Cloudy',    'rain': 70},
        'aurangabad':  {'temp': 29, 'humidity': 55, 'desc': 'Partly Cloudy',    'rain': 60},
        # Rajasthan
        'jaipur':      {'temp': 36, 'humidity': 28, 'desc': 'Hot and Dry',      'rain': 12},
        'jodhpur':     {'temp': 38, 'humidity': 22, 'desc': 'Arid',             'rain': 8},
        'udaipur':     {'temp': 31, 'humidity': 45, 'desc': 'Sunny',            'rain': 30},
        # UP / North
        'lucknow':     {'temp': 31, 'humidity': 62, 'desc': 'Partly Cloudy',    'rain': 60},
        'varanasi':    {'temp': 30, 'humidity': 68, 'desc': 'Humid',            'rain': 75},
        'agra':        {'temp': 33, 'humidity': 45, 'desc': 'Sunny',            'rain': 30},
        'kanpur':      {'temp': 32, 'humidity': 55, 'desc': 'Partly Cloudy',    'rain': 50},
        # Punjab / Haryana
        'amritsar':    {'temp': 28, 'humidity': 55, 'desc': 'Partly Cloudy',    'rain': 40},
        'chandigarh':  {'temp': 26, 'humidity': 60, 'desc': 'Pleasant',         'rain': 55},
        'ludhiana':    {'temp': 27, 'humidity': 58, 'desc': 'Partly Cloudy',    'rain': 45},
        # Bihar / Bengal
        'patna':       {'temp': 29, 'humidity': 72, 'desc': 'Humid',            'rain': 90},
        'kolkata':     {'temp': 30, 'humidity': 82, 'desc': 'Cloudy',           'rain': 130},
        'guwahati':    {'temp': 27, 'humidity': 85, 'desc': 'Rainy',            'rain': 180},
        # South India — Coastal / tropical
        'mumbai':      {'temp': 28, 'humidity': 88, 'desc': 'Humid and Coastal','rain': 200},
        'chennai':     {'temp': 34, 'humidity': 78, 'desc': 'Hot and Coastal',  'rain': 90},
        'bangalore':   {'temp': 24, 'humidity': 68, 'desc': 'Pleasant',         'rain': 85},
        'hyderabad':   {'temp': 31, 'humidity': 56, 'desc': 'Partly Cloudy',    'rain': 55},
        'kochi':       {'temp': 29, 'humidity': 92, 'desc': 'Tropical Humid',   'rain': 280},
        'thiruvananthapuram': {'temp': 28, 'humidity': 90, 'desc': 'Tropical',  'rain': 260},
        'coimbatore':  {'temp': 26, 'humidity': 72, 'desc': 'Partly Cloudy',    'rain': 95},
        'madurai':     {'temp': 33, 'humidity': 65, 'desc': 'Hot',              'rain': 70},
        'visakhapatnam':{'temp': 29, 'humidity': 80, 'desc': 'Coastal Humid',   'rain': 120},
        'mangalore':   {'temp': 28, 'humidity': 88, 'desc': 'Tropical Coastal', 'rain': 250},
        # Himalayan / Hilly regions
        'shimla':      {'temp': 12, 'humidity': 72, 'desc': 'Cool and Misty',   'rain': 120},
        'manali':      {'temp': 8,  'humidity': 65, 'desc': 'Cool Mountain',    'rain': 100},
        'dehradun':    {'temp': 20, 'humidity': 70, 'desc': 'Pleasant Hill',    'rain': 110},
        'mussoorie':   {'temp': 14, 'humidity': 75, 'desc': 'Misty Hill',       'rain': 130},
        'nainital':    {'temp': 13, 'humidity': 78, 'desc': 'Cool Hill Station','rain': 140},
        'darjeeling':  {'temp': 10, 'humidity': 85, 'desc': 'Misty and Cool',   'rain': 200},
        'srinagar':    {'temp': 14, 'humidity': 60, 'desc': 'Cool Valley',      'rain': 80},
        'leh':         {'temp': 5,  'humidity': 30, 'desc': 'Cold and Dry',     'rain': 15},
        # Gujarat
        'ahmedabad':   {'temp': 37, 'humidity': 36, 'desc': 'Hot',              'rain': 18},
        'surat':       {'temp': 30, 'humidity': 70, 'desc': 'Humid',            'rain': 80},
        'vadodara':    {'temp': 32, 'humidity': 55, 'desc': 'Partly Cloudy',    'rain': 40},
        # Odisha / Jharkhand
        'bhubaneswar': {'temp': 30, 'humidity': 76, 'desc': 'Humid',            'rain': 110},
        'ranchi':      {'temp': 25, 'humidity': 70, 'desc': 'Pleasant',         'rain': 90},
    }
    w = city_weather.get(city.lower(), {
        'temp': 28 + h % 12,
        'humidity': 50 + h % 30,
        'desc': 'Clear Sky',
        'rain': 40 + h % 60
    })
    return {
        'city':        city.title(),
        'temp':        w['temp'],
        'humidity':    w['humidity'],
        'description': w['desc'],
        'icon':        '01d',
        'wind':        12.5,
        'pressure':    1013,
        'feels_like':  w['temp'] - 2,
        'rainfall':    w['rain'],
        'success':     True,
        'demo':        True
    }


# ── Region classification ─────────────────────────────────────────────────────
COASTAL_CITIES = {
    'mumbai','chennai','kochi','thiruvananthapuram','visakhapatnam','mangalore',
    'goa','panaji','udupi','kozhikode','thrissur','kollam','alappuzha',
    'pondicherry','puducherry','karaikal','nagapattinam','rameswaram',
    'tuticorin','thoothukudi','bhubaneswar','puri','cuttack','paradip',
    'surat','dwarka','porbandar','veraval','bhavnagar','kandla',
    'ratnagiri','alibag','daman','silvassa',
}

HILLY_CITIES = {
    'shimla','manali','dehradun','mussoorie','nainital','darjeeling','srinagar',
    'leh','gangtok','shillong','aizawl','imphal','itanagar','kohima',
    'tawang','munnar','ooty','kodaikanal','coorg','chikmagalur',
    'dharamsala','mcleod ganj','dalhousie','kullu','mandi','bilaspur',
    'ranikhet','lansdowne','almora','pithoragarh','tehri',
}

ARID_CITIES = {
    'jodhpur','jaisalmer','bikaner','barmer','nagaur','churu',
    'ganganagar','hanumangarh','sikar','ajmer',
    'kutch','bhuj','anjar','mundra',
}

TROPICAL_WET_CITIES = {
    'kochi','thiruvananthapuram','kozhikode','thrissur','kollam','alappuzha',
    'mangalore','udupi','goa','panaji','margao',
    'guwahati','shillong','silchar','dibrugarh','jorhat','tezpur',
    'agartala','aizawl','imphal','kohima','itanagar',
    'darjeeling','kalimpong','siliguri',
}


def _get_region(city):
    c = city.lower().strip()
    if c in COASTAL_CITIES:      return 'coastal'
    if c in HILLY_CITIES:        return 'hilly'
    if c in ARID_CITIES:         return 'arid'
    if c in TROPICAL_WET_CITIES: return 'tropical_wet'
    return 'plains'


def get_soil_by_city(city):
    """
    Return soil parameters (N, P, K, ph) AND a region tag so the
    recommendation engine can bias towards regionally appropriate crops.
    """
    c = city.lower().strip()
    region = _get_region(c)

    # Base soil profiles per city
    city_soil = {
        # MP / Central
        'indore':      {'N':85,'P':45,'K':42,'ph':7.2},
        'bhopal':      {'N':78,'P':40,'K':38,'ph':7.0},
        'jabalpur':    {'N':90,'P':48,'K':45,'ph':6.8},
        'gwalior':     {'N':70,'P':35,'K':30,'ph':7.5},
        'ujjain':      {'N':75,'P':38,'K':34,'ph':7.3},
        # Maharashtra
        'mumbai':      {'N':60,'P':28,'K':22,'ph':6.3},
        'pune':        {'N':80,'P':42,'K':38,'ph':6.9},
        'nagpur':      {'N':68,'P':34,'K':28,'ph':7.1},
        'nashik':      {'N':72,'P':36,'K':32,'ph':6.8},
        'aurangabad':  {'N':70,'P':35,'K':30,'ph':7.0},
        # Rajasthan
        'jaipur':      {'N':55,'P':25,'K':20,'ph':8.0},
        'jodhpur':     {'N':40,'P':18,'K':15,'ph':8.4},
        'udaipur':     {'N':60,'P':28,'K':24,'ph':7.6},
        # UP / North
        'lucknow':     {'N':88,'P':46,'K':43,'ph':7.3},
        'varanasi':    {'N':85,'P':44,'K':40,'ph':7.1},
        'agra':        {'N':72,'P':36,'K':32,'ph':7.8},
        'kanpur':      {'N':80,'P':42,'K':38,'ph':7.2},
        # Punjab / Haryana
        'amritsar':    {'N':92,'P':50,'K':46,'ph':7.4},
        'chandigarh':  {'N':84,'P':44,'K':40,'ph':7.2},
        'ludhiana':    {'N':90,'P':48,'K':44,'ph':7.3},
        # Bihar / Bengal
        'patna':       {'N':92,'P':50,'K':48,'ph':6.7},
        'kolkata':     {'N':88,'P':52,'K':46,'ph':5.9},
        'guwahati':    {'N':82,'P':40,'K':36,'ph':5.8},
        # South — coastal / tropical
        'chennai':     {'N':68,'P':32,'K':28,'ph':6.4},
        'bangalore':   {'N':75,'P':38,'K':35,'ph':6.6},
        'hyderabad':   {'N':72,'P':36,'K':32,'ph':7.0},
        'kochi':       {'N':70,'P':30,'K':28,'ph':5.8},
        'thiruvananthapuram': {'N':65,'P':28,'K':24,'ph':5.7},
        'coimbatore':  {'N':74,'P':36,'K':32,'ph':6.5},
        'madurai':     {'N':70,'P':34,'K':30,'ph':6.8},
        'visakhapatnam':{'N':72,'P':34,'K':30,'ph':6.3},
        'mangalore':   {'N':68,'P':28,'K':26,'ph':5.6},
        # Hilly
        'shimla':      {'N':65,'P':30,'K':28,'ph':6.2},
        'manali':      {'N':58,'P':26,'K':22,'ph':6.0},
        'dehradun':    {'N':70,'P':34,'K':30,'ph':6.5},
        'mussoorie':   {'N':62,'P':28,'K':24,'ph':6.1},
        'nainital':    {'N':60,'P':26,'K':22,'ph':6.0},
        'darjeeling':  {'N':64,'P':28,'K':24,'ph':5.5},
        'srinagar':    {'N':68,'P':32,'K':28,'ph':6.8},
        'leh':         {'N':40,'P':18,'K':14,'ph':7.5},
        # Gujarat
        'ahmedabad':   {'N':60,'P':28,'K':22,'ph':7.8},
        'surat':       {'N':68,'P':32,'K':28,'ph':7.2},
        'vadodara':    {'N':70,'P':34,'K':30,'ph':7.4},
        # Odisha / Jharkhand
        'bhubaneswar': {'N':82,'P':42,'K':38,'ph':6.2},
        'ranchi':      {'N':76,'P':36,'K':32,'ph':5.9},
    }

    soil = city_soil.get(c, {'N':75,'P':38,'K':35,'ph':7.0}).copy()
    soil['region'] = region
    return soil


def get_regional_crop_bias(region):
    """
    Returns (preferred_crops, avoid_crops) lists based on region.
    These are used to boost/penalise crops in the recommendation score.
    """
    biases = {
        'coastal': {
            'prefer': ['coconut','banana','cashew','arecanut','pepper','cardamom',
                       'turmeric','ginger','rubber','rice','tapioca','arrowroot',
                       'pineapple','papaya','jackfruit','mango','guava',
                       'sugarcane','jute','brinjal','okra','bitter_gourd'],
            'avoid':  ['apple','strawberry','wheat','barley','mustard','linseed',
                       'safflower','lentil','chickpea','oats','ragi'],
        },
        'hilly': {
            'prefer': ['apple','strawberry','potato','peas','barley','oats',
                       'wheat','lentil','fieldpeas','ginger','turmeric',
                       'tea','cardamom','coffee','peach','plum',
                       'radish','cabbage','cauliflower','carrot','spinach',
                       'garlic','onion'],
            'avoid':  ['coconut','banana','sugarcane','cotton','jute','rubber',
                       'arecanut','pepper','tapioca','mango','papaya'],
        },
        'arid': {
            'prefer': ['bajra','mothbeans','horsegram','castor','sesame',
                       'groundnut','cumin','ajwain','fennel','coriander',
                       'sorghum','jowar','mustard','linseed','safflower',
                       'ber','neem','vetiver','aloe_vera','ashwagandha'],
            'avoid':  ['rice','jute','sugarcane','banana','coconut','tea',
                       'rubber','cardamom','pepper','lotus','brahmi'],
        },
        'tropical_wet': {
            'prefer': ['coconut','banana','rubber','pepper','cardamom',
                       'clove','arecanut','pineapple','jackfruit','papaya',
                       'rice','tapioca','arrowroot','yam','ginger',
                       'turmeric','black pepper','tea','coffee','sugarcane',
                       'jute','lotus','brahmi'],
            'avoid':  ['apple','barley','oats','wheat','lentil','chickpea',
                       'mustard','bajra','mothbeans','ajwain','cumin'],
        },
        'plains': {
            'prefer': ['wheat','rice','maize','sugarcane','cotton','soybean',
                       'mustard','chickpea','lentil','pigeonpeas','mungbean',
                       'blackgram','onion','potato','tomato','marigold'],
            'avoid':  [],
        },
    }
    return biases.get(region, biases['plains'])


def get_weather_forecast(city, api_key=None):
    """Get 7-day weather forecast from OpenWeatherMap."""
    if not api_key:
        from django.conf import settings
        api_key = getattr(settings, 'OPENWEATHER_API_KEY', '')

    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city},IN&appid={api_key}&units=metric&cnt=40"
        r = __import__('requests').get(url, timeout=6)
        if r.status_code == 200:
            data = r.json()
            days = {}
            for item in data['list']:
                import datetime
                date = datetime.datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                if date not in days:
                    days[date] = {
                        'date': date,
                        'day': datetime.datetime.fromtimestamp(item['dt']).strftime('%a'),
                        'temp_max': item['main']['temp_max'],
                        'temp_min': item['main']['temp_min'],
                        'humidity': item['main']['humidity'],
                        'description': item['weather'][0]['description'].title(),
                        'icon': item['weather'][0]['icon'],
                        'rain': item.get('rain', {}).get('3h', 0),
                    }
                else:
                    days[date]['temp_max'] = max(days[date]['temp_max'], item['main']['temp_max'])
                    days[date]['temp_min'] = min(days[date]['temp_min'], item['main']['temp_min'])
            forecast = list(days.values())[:7]
            for d in forecast:
                d['temp_max'] = round(d['temp_max'], 1)
                d['temp_min'] = round(d['temp_min'], 1)
            return {'success': True, 'city': data['city']['name'], 'forecast': forecast}
    except Exception:
        pass
    return _mock_forecast(city)


def _mock_forecast(city):
    import datetime, hashlib
    h = int(hashlib.md5(city.encode()).hexdigest(), 16) % 10
    w = _mock_weather(city)
    base_temp = w['temp']
    days = []
    descs = ['Clear Sky','Partly Cloudy','Scattered Clouds','Sunny','Light Rain','Clear Sky','Partly Cloudy']
    for i in range(7):
        d = datetime.date.today() + datetime.timedelta(days=i)
        variation = ((h + i) % 5) - 2
        days.append({
            'date': d.strftime('%Y-%m-%d'),
            'day': d.strftime('%a'),
            'temp_max': round(base_temp + variation + 2, 1),
            'temp_min': round(base_temp + variation - 4, 1),
            'humidity': min(95, max(20, w['humidity'] + (i % 3 - 1) * 5)),
            'description': descs[i],
            'icon': '01d',
            'rain': [0,0,2,0,5,0,0][i],
        })
    return {'success': True, 'city': city.title(), 'forecast': days, 'demo': True}


def get_mandi_prices_live(crop, state='', limit=10):
    """
    Fetch real mandi prices from data.gov.in Agmarknet API.
    Resource ID: 9ef84268-d588-465a-a308-a864a43d0070
    Returns list of market prices for the given crop.
    """
    import requests as req
    from django.conf import settings

    api_key = getattr(settings, 'DATA_GOV_API_KEY', '')
    if not api_key:
        return {'success': False, 'live': False, 'error': 'No API key'}

    # Commodity name mapping (our names → Agmarknet names)
    COMMODITY_MAP = {
        'rice': 'Rice', 'wheat': 'Wheat', 'maize': 'Maize',
        'bajra': 'Bajra(Pearl Millet/Cumbu)', 'sorghum': 'Jowar(Sorghum)',
        'jowar': 'Jowar(Sorghum)', 'ragi': 'Ragi (Finger Millet)',
        'cotton': 'Cotton', 'sugarcane': 'Sugarcane',
        'soybean': 'Soyabean', 'groundnut': 'Groundnut',
        'mustard': 'Mustard', 'sunflower': 'Sunflower Seed',
        'onion': 'Onion', 'potato': 'Potato', 'tomato': 'Tomato',
        'garlic': 'Garlic', 'chilli': 'Dry Chillies',
        'turmeric': 'Turmeric', 'ginger': 'Ginger(Dry)',
        'chickpea': 'Gram', 'lentil': 'Lentil', 'mungbean': 'Moong(Whole)',
        'blackgram': 'Black Gram (Urd Beans)(Whole)',
        'pigeonpeas': 'Arhar (Tur/Red Gram)(Whole)',
        'banana': 'Banana', 'mango': 'Mango', 'papaya': 'Papaya',
        'coconut': 'Coconut', 'orange': 'Orange', 'apple': 'Apple',
        'grapes': 'Grapes', 'pomegranate': 'Pomegranate',
        'watermelon': 'Water Melon', 'guava': 'Guava',
        'brinjal': 'Brinjal', 'okra': 'Bhindi(Ladies Finger)',
        'cabbage': 'Cabbage', 'cauliflower': 'Cauliflower',
        'peas': 'Peas Wet', 'carrot': 'Carrot', 'radish': 'Raddish',
        'spinach': 'Spinach', 'bitter_gourd': 'Bitter Gourd',
        'bottle_gourd': 'Bottle Gourd', 'cucumber': 'Cucumber',
        'pepper': 'Pepper ungarbled', 'cardamom': 'Cardamom',
        'coffee': 'Coffee', 'tea': 'Tea',
        'jute': 'Jute', 'barley': 'Barley',
        'sesame': 'Sesamum(Sesame/Gingelly)', 'linseed': 'Linseed',
        'castor': 'Castor Seed', 'safflower': 'Safflower',
    }

    commodity = COMMODITY_MAP.get(crop.lower(), crop.title())

    try:
        url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
        params = {
            'api-key': api_key,
            'format': 'json',
            'limit': limit,
            'filters[Commodity]': commodity,
        }
        if state:
            params['filters[State]'] = state.title()

        r = req.get(url, params=params, timeout=8)
        if r.status_code == 200:
            data = r.json()
            records = data.get('records', [])
            if records:
                prices = []
                for rec in records:
                    try:
                        prices.append({
                            'market':      rec.get('Market', '—'),
                            'district':    rec.get('District', '—'),
                            'state':       rec.get('State', '—'),
                            'commodity':   rec.get('Commodity', commodity),
                            'variety':     rec.get('Variety', '—'),
                            'min_price':   int(float(rec.get('Min_Price', 0))),
                            'max_price':   int(float(rec.get('Max_Price', 0))),
                            'modal_price': int(float(rec.get('Modal_Price', 0))),
                            'date':        rec.get('Arrival_Date', '—'),
                        })
                    except Exception:
                        continue
                return {
                    'success': True,
                    'live': True,
                    'crop': crop,
                    'commodity': commodity,
                    'prices': prices,
                    'total': data.get('total', len(prices)),
                }
        return {'success': False, 'live': False, 'error': f'API returned {r.status_code}'}
    except Exception as e:
        return {'success': False, 'live': False, 'error': str(e)[:100]}