import pickle, os, numpy as np

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'ml_models')
_model = _le = _scaler = None

# Season and water encodings (must match train_model.py)
_SEASON_ENC = {}
_WATER_ENC  = {'Very Low':0,'Low':1,'Low-Medium':1.5,'Medium':2,'High':3,'Very High':4}

def _build_encodings():
    global _SEASON_ENC
    for crop, info in CROP_INFO.items():
        s = info.get('season','')
        if 'Kharif' in s:   _SEASON_ENC[crop] = 0.0
        elif 'Rabi' in s:   _SEASON_ENC[crop] = 1.0
        elif 'Zaid' in s:   _SEASON_ENC[crop] = 2.0
        else:               _SEASON_ENC[crop] = 1.5

def _load():
    global _model, _le, _scaler
    if _model is None:
        model_path = os.path.join(MODEL_DIR, 'crop_model.pkl')
        if not os.path.exists(model_path):
            from core.ml_models.train_model import train_and_save
            train_and_save()
        with open(os.path.join(MODEL_DIR,'crop_model.pkl'),'rb') as f: _model=pickle.load(f)
        with open(os.path.join(MODEL_DIR,'label_encoder.pkl'),'rb') as f: _le=pickle.load(f)
        with open(os.path.join(MODEL_DIR,'scaler.pkl'),'rb') as f: _scaler=pickle.load(f)
        _build_encodings()

# ─── SEASON KEY ───────────────────────────────────────────────────────────────
# Kharif = June–Oct (monsoon)   Rabi = Oct–Mar (winter)   Zaid = Mar–Jun (summer)
# ──────────────────────────────────────────────────────────────────────────────

CROP_INFO = {
    # ── CEREALS ──
    'rice':            {'emoji':'🌾','season':'Kharif','water':'High',       'time':'90-120 days', 'tips':['Maintain 5 cm standing water','Transplant at 21 days','Monitor for blast disease']},
    'wheat':           {'emoji':'🌾','season':'Rabi',  'water':'Medium',     'time':'110-130 days','tips':['Timely sowing is critical','Apply first irrigation at CRI stage','Monitor for rust']},
    'maize':           {'emoji':'🌽','season':'Kharif','water':'Medium',     'time':'60-90 days',  'tips':['Plant at 75 cm row spacing','Apply Urea in splits','Watch for stem borer']},
    'barley':          {'emoji':'🌾','season':'Rabi',  'water':'Low',        'time':'90-110 days', 'tips':['Drought tolerant cereal','Apply 60 kg N/ha','Harvest at dough stage']},
    'sorghum':         {'emoji':'🌾','season':'Kharif','water':'Low-Medium', 'time':'90-120 days', 'tips':['Deep rooted drought-tolerant crop','Avoid water stagnation','Threshing after drying']},
    'bajra':           {'emoji':'🌾','season':'Kharif','water':'Low',        'time':'75-90 days',  'tips':['Best for sandy loam soils','Requires warm temperatures','Harvest when 80% grains harden']},
    'ragi':            {'emoji':'🌾','season':'Kharif','water':'Low',        'time':'90-120 days', 'tips':['Nutritionally rich millet','Tolerates low fertility soils','Finger millet harvested at maturity']},
    'jowar':           {'emoji':'🌾','season':'Kharif','water':'Low-Medium', 'time':'100-120 days','tips':['Dual-purpose grain and fodder','Avoid acidic soils','Apply 40 kg N at sowing']},
    'oats':            {'emoji':'🌾','season':'Rabi',  'water':'Low-Medium', 'time':'90-120 days', 'tips':['Excellent fodder crop','Sow in Oct-Nov','Cut at milky stage for fodder']},
    'triticale':       {'emoji':'🌾','season':'Rabi',  'water':'Medium',     'time':'110-130 days','tips':['Wheat-rye hybrid','Better than wheat on poor soils','Good for bread and fodder']},

    # ── PULSES ──
    'chickpea':        {'emoji':'🫘','season':'Rabi',  'water':'Low',        'time':'90-110 days', 'tips':['Inoculate with Rhizobium','Avoid waterlogging','Harvest when pods turn brown']},
    'kidneybeans':     {'emoji':'🫘','season':'Kharif','water':'Medium',     'time':'80-100 days', 'tips':['Support with stakes','Avoid overhead watering','Pick pods before full maturity']},
    'pigeonpeas':      {'emoji':'🌿','season':'Kharif','water':'Low',        'time':'150-180 days','tips':['Deep plowing before sowing','Intercrop with sorghum','Harvest in stages']},
    'mothbeans':       {'emoji':'🫘','season':'Kharif','water':'Very Low',   'time':'60-75 days',  'tips':['Drought tolerant crop','Sandy loam soil ideal','Minimal irrigation needed']},
    'mungbean':        {'emoji':'🌱','season':'Zaid',  'water':'Low',        'time':'60-75 days',  'tips':['Short duration summer crop','Good for soil health','Pick green pods early']},
    'blackgram':       {'emoji':'🫘','season':'Kharif','water':'Low',        'time':'70-80 days',  'tips':['Requires warm humid climate','Avoid acidic soils','Rotate with cereals']},
    'lentil':          {'emoji':'🫘','season':'Rabi',  'water':'Low',        'time':'90-110 days', 'tips':['Cool weather crop','Avoid excessive nitrogen','Harvest at 80% pod maturity']},
    'fieldpeas':       {'emoji':'🫛','season':'Rabi',  'water':'Low-Medium', 'time':'90-120 days', 'tips':['Cool season legume','Fix atmospheric nitrogen','Harvest when pods are full']},
    'cowpea':          {'emoji':'🫘','season':'Kharif','water':'Low',        'time':'60-90 days',  'tips':['Multi-purpose legume','Tolerates heat and drought','Harvest pods at green stage']},
    'horsegram':       {'emoji':'🫘','season':'Rabi',  'water':'Very Low',   'time':'90-120 days', 'tips':['Grown in dry regions','No supplemental irrigation needed','High protein legume']},
    'soybean':         {'emoji':'🫘','season':'Kharif','water':'Medium',     'time':'90-120 days', 'tips':['Inoculate with Bradyrhizobium','Row spacing 45 cm','Harvest at 13% moisture']},
    'groundnut':       {'emoji':'🥜','season':'Kharif','water':'Medium',     'time':'90-120 days', 'tips':['Gypsum at pegging improves yield','Earthing up for pod development','Dry pods to 10% moisture']},

    # ── OILSEEDS ──
    'mustard':         {'emoji':'🌼','season':'Rabi',  'water':'Low-Medium', 'time':'90-110 days', 'tips':['Sow in Oct-Nov for best yield','Apply sulfur fertilizer','Harvest when 75% pods turn yellow']},
    'sunflower':       {'emoji':'🌻','season':'Zaid',  'water':'Medium',     'time':'90-110 days', 'tips':['Needs full sunlight','Irrigate at flowering and seed fill','Harvest when back of head turns brown']},
    'sesame':          {'emoji':'🌿','season':'Kharif','water':'Low',        'time':'75-90 days',  'tips':['Drought tolerant oilseed','Thin to one plant per hill','Harvest before pods shatter']},
    'linseed':         {'emoji':'🌿','season':'Rabi',  'water':'Low-Medium', 'time':'100-120 days','tips':['Omega-3 rich crop','Suits cold dry areas','Rogue off-types for purity']},
    'safflower':       {'emoji':'🌼','season':'Rabi',  'water':'Low',        'time':'130-150 days','tips':['Deep-rooted drought crop','Grows on black cotton soils','Harvest heads when dry']},
    'castor':          {'emoji':'🌿','season':'Kharif','water':'Low-Medium', 'time':'120-150 days','tips':['Grows on marginal lands','Never waterlog roots','Harvest capsules before splitting']},
    'rapeseed':        {'emoji':'🌼','season':'Rabi',  'water':'Low-Medium', 'time':'90-110 days', 'tips':['Similar to mustard in management','Rich in glucosinolates','Apply boron micronutrient']},

    # ── FIBER CROPS ──
    'cotton':          {'emoji':'☁️','season':'Kharif','water':'Medium',     'time':'150-180 days','tips':['Use BT cotton varieties','Scout for bollworm weekly','Apply foliar urea at boll stage']},
    'jute':            {'emoji':'🌿','season':'Kharif','water':'High',       'time':'100-120 days','tips':['Flood plain soils ideal','Ret for 10-20 days','Pull weeds at 3-4 weeks']},
    'hemp':            {'emoji':'🌿','season':'Kharif','water':'Low-Medium', 'time':'90-120 days', 'tips':['Grows in well-drained soils','Weed-suppressing crop','Harvest at early flowering']},
    'flax':            {'emoji':'🌿','season':'Rabi',  'water':'Low',        'time':'90-110 days', 'tips':['Dual-purpose fiber and oil','Thin to 15 cm apart','Pull by hand at ripening']},

    # ── SUGAR CROPS ──
    'sugarcane':       {'emoji':'🌿','season':'Kharif','water':'High',       'time':'12-18 months','tips':['Ratoon management saves cost','Trash mulching conserves moisture','Apply Trichoderma for disease']},
    'sugarbeet':       {'emoji':'🌱','season':'Rabi',  'water':'Medium',     'time':'150-180 days','tips':['Suited for temperate regions','Harvest before frost','Stores well at low temperatures']},
    'sweetpotato':     {'emoji':'🍠','season':'Kharif','water':'Medium',     'time':'90-120 days', 'tips':['Ridge planting improves yield','Harvest carefully to avoid damage','Cure at 30°C before storage']},

    # ── ROOT & TUBER ──
    'potato':          {'emoji':'🥔','season':'Rabi',  'water':'Medium',     'time':'75-100 days', 'tips':['Plant certified seed tubers','Earth up at 30 days','Harvest when skin sets firm']},
    'tapioca':         {'emoji':'🌿','season':'Kharif','water':'Low-Medium', 'time':'9-12 months', 'tips':['Stake tall varieties','Apply K heavily for starch','Harvest at 9+ months']},
    'arrowroot':       {'emoji':'🌿','season':'Kharif','water':'Medium',     'time':'9-11 months', 'tips':['Shaded conditions ideal','Grows in laterite soils','Extract starch immediately after harvest']},
    'yam':             {'emoji':'🍠','season':'Kharif','water':'Medium',     'time':'180-240 days','tips':['Stake yam vines','Mulch heavily at planting','Harvest after leaves senesce']},

    # ── VEGETABLES ──
    'onion':           {'emoji':'🧅','season':'Rabi',  'water':'Medium',     'time':'90-120 days', 'tips':['Transplant 45-day-old seedlings','Stop irrigation 15 days before harvest','Cure bulbs in shade for 7-10 days']},
    'garlic':          {'emoji':'🧄','season':'Rabi',  'water':'Low-Medium', 'time':'130-160 days','tips':['Plant individual cloves 5 cm deep','Avoid excess nitrogen','Harvest when 50% leaves turn yellow']},
    'tomato':          {'emoji':'🍅','season':'Zaid',  'water':'Medium',     'time':'60-90 days',  'tips':['Stake or cage plants','Apply Ca spray to prevent blossom-end rot','Harvest when fully red']},
    'potato_veg':      {'emoji':'🥔','season':'Rabi',  'water':'Medium',     'time':'75-100 days', 'tips':['Use disease-free seed','Hill up soil around plants','Harvest after foliage dies']},
    'chilli':          {'emoji':'🌶️','season':'Kharif','water':'Medium',     'time':'90-150 days', 'tips':['Grow transplants in nursery','Apply K for pungency','Harvest at red ripe stage for drying']},
    'brinjal':         {'emoji':'🍆','season':'Kharif','water':'Medium',     'time':'90-120 days', 'tips':['Stake tall varieties','Monitor shoot-and-fruit borer','Harvest at glossy purple stage']},
    'okra':            {'emoji':'🌿','season':'Zaid',  'water':'Medium',     'time':'50-65 days',  'tips':['Direct sow in well-drained soil','Harvest every 2-3 days','Apply 30 kg N/ha']},
    'peas':            {'emoji':'🫛','season':'Rabi',  'water':'Low-Medium', 'time':'60-90 days',  'tips':['Sow in rows of 30 cm','Provide trellis support','Harvest when pods are plump']},
    'cabbage':         {'emoji':'🥬','season':'Rabi',  'water':'Medium',     'time':'90-120 days', 'tips':['Transplant 4-week seedlings','Apply 120 kg N/ha in splits','Harvest before heads crack']},
    'cauliflower':     {'emoji':'🥦','season':'Rabi',  'water':'Medium',     'time':'90-120 days', 'tips':['Tie outer leaves over curd','Apply boron for solid curds','Harvest when curd is compact']},
    'carrot':          {'emoji':'🥕','season':'Rabi',  'water':'Medium',     'time':'75-100 days', 'tips':['Deep loose sandy soil ideal','Thin to 5 cm spacing','Harvest before roots crack']},
    'radish':          {'emoji':'🌱','season':'Zaid',  'water':'Low-Medium', 'time':'25-40 days',  'tips':['Quick rotation crop','Sow every 2 weeks for continuous harvest','Pull before roots turn pithy']},
    'spinach':         {'emoji':'🥬','season':'Rabi',  'water':'Medium',     'time':'30-45 days',  'tips':['High nitrogen demand','Cut-and-come-again harvesting','Avoid summer heat — bolts quickly']},
    'fenugreek':       {'emoji':'🌿','season':'Rabi',  'water':'Low-Medium', 'time':'25-30 days',  'tips':['Used as leafy vegetable','Grows in well-drained loam','Harvest young leaves frequently']},
    'bitter_gourd':    {'emoji':'🌿','season':'Zaid',  'water':'Medium',     'time':'55-70 days',  'tips':['Train on overhead pandal','Harvest young green fruits','Apply 40 kg K/ha']},
    'bottle_gourd':    {'emoji':'🫙','season':'Zaid',  'water':'Medium',     'time':'55-70 days',  'tips':['Needs warm weather','Harvest tender fruits at 15-20 cm','Water regularly at fruiting']},
    'ridge_gourd':     {'emoji':'🌿','season':'Zaid',  'water':'Medium',     'time':'50-60 days',  'tips':['Trellis essential','Harvest before fibers harden','Grows well in sandy loam']},
    'pumpkin':         {'emoji':'🎃','season':'Kharif','water':'Medium',     'time':'90-120 days', 'tips':['Allow 2-3 m2 per plant','Harvest when stem dries','Stores well at cool dry conditions']},
    'cucumber':        {'emoji':'🥒','season':'Zaid',  'water':'Medium',     'time':'45-60 days',  'tips':['Trellis for better fruit','Harvest at dark green stage','Keep soil evenly moist']},

    # ── FRUITS ──
    'pomegranate':     {'emoji':'🍎','season':'Zaid',  'water':'Low-Medium', 'time':'2-3 years',   'tips':['Prune for open canopy','Apply potash for fruit quality','Protect from fruit borer']},
    'banana':          {'emoji':'🍌','season':'Kharif','water':'High',       'time':'10-15 months','tips':['Plant in rows of 1.8 m','Remove side shoots','Bunch cover for quality']},
    'mango':           {'emoji':'🥭','season':'Zaid',  'water':'Low-Medium', 'time':'3-5 years',   'tips':['Graft for early fruiting','Apply Paclobutrazol for flowering','Control powdery mildew']},
    'grapes':          {'emoji':'🍇','season':'Rabi',  'water':'Medium',     'time':'3 years',     'tips':['Train on bower/trellis','Prune annually','Thin bunches for quality']},
    'watermelon':      {'emoji':'🍉','season':'Zaid',  'water':'Medium',     'time':'70-85 days',  'tips':['Sandy loam is ideal','Use mulch for moisture','Hand pollinate for better fruit set']},
    'muskmelon':       {'emoji':'🍈','season':'Zaid',  'water':'Medium',     'time':'75-90 days',  'tips':['Trellis training helps','Drip irrigation preferred','Harvest at slip stage']},
    'apple':           {'emoji':'🍎','season':'Rabi',  'water':'Medium',     'time':'4-5 years',   'tips':['Requires chilling hours','Thin fruits for size','Spray calcium for firmness']},
    'orange':          {'emoji':'🍊','season':'Zaid',  'water':'Medium',     'time':'3-5 years',   'tips':['Deep feeder roots','Apply micronutrients','Control citrus psylla']},
    'papaya':          {'emoji':'🍑','season':'Zaid',  'water':'Medium',     'time':'8-10 months', 'tips':['Plant on raised beds','Stake young plants','Protect from PRSV virus']},
    'coconut':         {'emoji':'🥥','season':'Kharif','water':'High',       'time':'6-8 years',   'tips':['Apply green manure','Control rhinoceros beetle','Basin irrigation is best']},
    'guava':           {'emoji':'🍐','season':'Zaid',  'water':'Low-Medium', 'time':'2-3 years',   'tips':['Tolerates a wide range of soils','Prune after harvest','Monitor for wilt disease']},
    'litchi':          {'emoji':'🍒','season':'Zaid',  'water':'High',       'time':'5-7 years',   'tips':['Needs cool dry winters','Ring bagging protects fruits','Harvest in clusters']},
    'jackfruit':       {'emoji':'🍈','season':'Kharif','water':'Medium',     'time':'5-7 years',   'tips':['Tolerates poor soils','Fruits on trunk and main branches','Harvest at hollow sound stage']},
    'pineapple':       {'emoji':'🍍','season':'Kharif','water':'Medium',     'time':'15-18 months','tips':['Plant suckers or crowns','Use mulch to suppress weeds','Ethephon for uniform flowering']},
    'strawberry':      {'emoji':'🍓','season':'Rabi',  'water':'Medium',     'time':'90-120 days', 'tips':['Raised bed planting','Use drip and mulch together','Harvest every 2 days at peak']},
    'amla':            {'emoji':'🫒','season':'Kharif','water':'Low',        'time':'5-8 years',   'tips':['Highly drought tolerant','Prune crossing branches','Harvest Nov-Feb for best quality']},
    'ber':             {'emoji':'🫐','season':'Kharif','water':'Very Low',   'time':'3-5 years',   'tips':['Grows on marginal land','Head back pruning every year','Harvest at yellow-green stage']},
    'tamarind':        {'emoji':'🌿','season':'Kharif','water':'Low',        'time':'7-10 years',  'tips':['Drought hardy tree','Minimal care once established','Harvest pods when shell turns brown']},
    'jamun':           {'emoji':'🫐','season':'Kharif','water':'Low-Medium', 'time':'5-7 years',   'tips':['Medicinal value high','Bird netting at fruiting','Harvest when fully purple']},
    'custard_apple':   {'emoji':'🍏','season':'Kharif','water':'Low-Medium', 'time':'3-4 years',   'tips':['Hand pollinate for better fruit set','Harvest when skin starts cracking','Rich in antioxidants']},
    'sapota':          {'emoji':'🟤','season':'Zaid',  'water':'Medium',     'time':'4-5 years',   'tips':['Sensitive to frost','Harvest when skin turns dull brown','Ripen off-tree at room temp']},
    'fig':             {'emoji':'🫐','season':'Rabi',  'water':'Low',        'time':'2-3 years',   'tips':['Prune to open shape','2 crops/year in warm climate','Harvest when fully soft']},
    'mulberry':        {'emoji':'🫐','season':'Kharif','water':'Medium',     'time':'2-3 years',   'tips':['Grown for silkworm rearing','Harvest leaves 3-4 times/year','Apply 200 kg N/ha/year']},

    # ── PLANTATION ──
    'coffee':          {'emoji':'☕','season':'Kharif','water':'Medium',     'time':'3-4 years',   'tips':['Shade growing preferred','Prune after harvest','Wet processing for quality']},
    'tea':             {'emoji':'🍵','season':'Kharif','water':'High',       'time':'3-5 years',   'tips':['Requires acidic soil pH 4.5-5.5','Pluck 2 leaves and a bud','Apply 150 kg N/ha/year']},
    'rubber':          {'emoji':'🌿','season':'Kharif','water':'High',       'time':'6-7 years',   'tips':['Tapping starts at 5-6 years','Tap early morning','Apply latex stimulants carefully']},
    'cashew':          {'emoji':'🥜','season':'Zaid',  'water':'Low',        'time':'3-5 years',   'tips':['Tolerates laterite soils','Apply 4:2:4 NPK fertilizer','Harvest fallen nuts daily']},
    'arecanut':        {'emoji':'🌴','season':'Kharif','water':'High',       'time':'7-8 years',   'tips':['Drip irrigation most efficient','Control Mahali disease with copper','Harvest bunches at yellow stage']},
    'clove':           {'emoji':'🌸','season':'Kharif','water':'Medium',     'time':'6-8 years',   'tips':['Grows in humid tropics','Harvest buds before they open','Dry in sun for 4-5 days']},
    'cardamom':        {'emoji':'🌿','season':'Kharif','water':'High',       'time':'3-4 years',   'tips':['Grows under shade','Harvest capsules just before ripening','Cure in electric dryer at 50°C']},
    'pepper':          {'emoji':'🌶️','season':'Kharif','water':'High',       'time':'3-4 years',   'tips':['Train on standard trees','Harvest at semi-ripe stage','Dry in sun for 3-5 days']},
    'turmeric':        {'emoji':'🟡','season':'Kharif','water':'High',       'time':'7-9 months',  'tips':['Plant rhizomes 5 cm deep','Earth up at 45 days','Harvest when leaves turn yellow']},
    'ginger':          {'emoji':'🫚','season':'Kharif','water':'High',       'time':'8-9 months',  'tips':['Plant at 15x25 cm spacing','Mulch heavily with leaves','Harvest after foliage dries']},

    # ── FORAGE / GREEN MANURE ──
    'lucerne':         {'emoji':'🌿','season':'Rabi',  'water':'Medium',     'time':'60-90 days',  'tips':['High protein fodder','4-6 cuts per season','Inoculate with Rhizobium']},
    'berseem':         {'emoji':'🌿','season':'Rabi',  'water':'Medium',     'time':'45-60 days',  'tips':['Best winter fodder','5-6 cuts per season','Apply phosphorus at sowing']},
    'napier_grass':    {'emoji':'🌿','season':'Kharif','water':'Medium',     'time':'Perennial',   'tips':['Grows 3-4 m tall','Cut at 45-day intervals','Apply 100 kg N/ha/year']},
    'dhaincha':        {'emoji':'🌿','season':'Zaid',  'water':'Low',        'time':'50-60 days',  'tips':['Excellent green manure','Plough in before flowering','Fixes 80-100 kg N/ha']},
    'sunhemp':         {'emoji':'🌿','season':'Kharif','water':'Low',        'time':'45-60 days',  'tips':['Fast-growing green manure','Incorporate at 50% flowering','Improves soil structure']},

    # ── SPICES ──
    'coriander':       {'emoji':'🌿','season':'Rabi',  'water':'Low-Medium', 'time':'90-100 days', 'tips':['Soak seeds overnight before sowing','Harvest seeds when brown','Apply 30 kg N/ha']},
    'cumin':           {'emoji':'🌿','season':'Rabi',  'water':'Low',        'time':'90-120 days', 'tips':['Grows in dry cool climate','3 irrigations sufficient','Harvest when 70% seeds turn brown']},
    'ajwain':          {'emoji':'🌿','season':'Rabi',  'water':'Low',        'time':'90-100 days', 'tips':['Sandy loam soils ideal','Thin to 30 cm spacing','Harvest umbels when turning brown']},
    'fennel':          {'emoji':'🌿','season':'Rabi',  'water':'Low-Medium', 'time':'150-180 days','tips':['Deep friable soil needed','Harvest in early morning','Dry in shade to retain aroma']},
    'dill':            {'emoji':'🌿','season':'Rabi',  'water':'Low',        'time':'70-90 days',  'tips':['Direct sow in cool season','Harvest seeds when turning brown','Avoid waterlogging']},

    # ── FLOWERS ──
    'rose':            {'emoji':'🌹','season':'Zaid',  'water':'Medium',     'time':'3-5 months',  'tips':['Apply 6-6-6 NPK monthly','Prune after each flush','Spray fungicide for black spot']},
    'marigold':        {'emoji':'🌸','season':'Kharif','water':'Low-Medium', 'time':'60-80 days',  'tips':['Direct sow or transplant','Deadhead for continuous blooms','Used as trap crop for pests']},
    'jasmine':         {'emoji':'🌼','season':'Zaid',  'water':'Medium',     'time':'2-3 years',   'tips':['Train on trellis or fence','Harvest flowers at bud stage','Apply FYM annually']},
    'chrysanthemum':   {'emoji':'🌼','season':'Rabi',  'water':'Medium',     'time':'90-120 days', 'tips':['Pinch at 4-6 leaf stage','Short day plant — needs dark period','Harvest at half-open stage']},
    'tuberose':        {'emoji':'🌸','season':'Kharif','water':'Medium',     'time':'90-120 days', 'tips':['Plant bulbs 5 cm deep','Apply K for fragrance','Harvest spikes at 2-3 florets open']},
    'lotus':           {'emoji':'🪷','season':'Kharif','water':'Very High',  'time':'3-4 months',  'tips':['Grows in ponds and wetlands','Harvest rhizomes in winter','Flowers in morning — harvest early']},

    # ── MEDICINAL ──
    'aloe_vera':       {'emoji':'🌵','season':'Zaid',  'water':'Very Low',   'time':'8-18 months', 'tips':['Sandy well-drained soil ideal','Harvest outer leaves first','Apply potassium for gel quality']},
    'ashwagandha':     {'emoji':'🌿','season':'Kharif','water':'Low',        'time':'150-180 days','tips':['Sandy loam soils only','Minimum irrigation needed','Harvest roots when leaves wither']},
    'stevia':          {'emoji':'🌿','season':'Zaid',  'water':'Medium',     'time':'3-4 months',  'tips':['Harvest before flowering','Dry leaves in shade','4-5 cuts per year possible']},
    'lemongrass':      {'emoji':'🌿','season':'Kharif','water':'Low-Medium', 'time':'6-8 months',  'tips':['Propagate by stem division','3-4 cuts per year','Distill for essential oil']},
    'tulsi':           {'emoji':'🌿','season':'Kharif','water':'Low',        'time':'3-4 months',  'tips':['Sacred and medicinal plant','Harvest before full flowering','Rich in essential oils']},
    'neem':            {'emoji':'🌳','season':'Kharif','water':'Very Low',   'time':'5-7 years',   'tips':['Drought hardy tree','Seeds used for biopesticide','Grows in degraded soils']},
    'brahmi':          {'emoji':'🌿','season':'Kharif','water':'High',       'time':'3-4 months',  'tips':['Grows near water bodies','Propagate by stem cutting','Harvest young shoots']},

    # ── MISCELLANEOUS ──
    'indigo':          {'emoji':'🌿','season':'Kharif','water':'Medium',     'time':'90-120 days', 'tips':['Natural blue dye crop','Harvest before pods mature','Multiple cuts possible']},
    'tobacco':         {'emoji':'🍃','season':'Rabi',  'water':'Medium',     'time':'90-120 days', 'tips':['Transplant 6-week seedlings','Harvest leaves from bottom up','Cure in barns at 35-70°C']},
    'hop':             {'emoji':'🌿','season':'Kharif','water':'Medium',     'time':'3 years',     'tips':['Train on 6 m high strings','Harvest cones at aroma peak','Needs long days for cone production']},
    'vetiver':         {'emoji':'🌿','season':'Kharif','water':'Low',        'time':'6-8 months',  'tips':['Excellent for soil conservation','Roots go 3-4 m deep','Essential oil extracted from roots']},
}

# ── MSP PRICES (₹/quintal, Govt. of India 2023-24) ──────────────────────────
MANDI_PRICES = {
    'rice':2183,'wheat':2275,'maize':1962,'barley':1735,'sorghum':3180,
    'bajra':2500,'ragi':3846,'jowar':3180,'oats':1900,'triticale':1800,
    'chickpea':5440,'kidneybeans':6000,'pigeonpeas':7000,'mothbeans':6573,
    'mungbean':8558,'blackgram':6950,'lentil':6425,'fieldpeas':5350,
    'cowpea':5500,'horsegram':4500,'soybean':4600,'groundnut':6377,
    'mustard':5650,'sunflower':6760,'sesame':8635,'linseed':5500,
    'safflower':5800,'castor':6170,'rapeseed':5650,
    'cotton':6620,'jute':5050,'hemp':5000,'flax':4500,
    'sugarcane':315,'sugarbeet':2800,'sweetpotato':1500,
    'potato':800,'tapioca':2000,'arrowroot':3000,'yam':2500,
    'onion':1500,'garlic':6000,'tomato':1200,'chilli':9000,'brinjal':1000,
    'okra':1500,'peas':2500,'cabbage':800,'cauliflower':1200,'carrot':1500,
    'radish':800,'spinach':1000,'fenugreek':5000,'bitter_gourd':1800,
    'bottle_gourd':900,'ridge_gourd':1200,'pumpkin':900,'cucumber':1000,
    'pomegranate':8000,'banana':1500,'mango':4000,'grapes':7000,
    'watermelon':800,'muskmelon':1200,'apple':8000,'orange':3500,
    'papaya':1500,'coconut':1800,'guava':2000,'litchi':6000,
    'jackfruit':2000,'pineapple':3000,'strawberry':5000,'amla':3500,
    'ber':2500,'tamarind':5000,'jamun':3000,'custard_apple':4000,
    'sapota':3000,'fig':6000,'mulberry':2000,
    'coffee':18000,'tea':15000,'rubber':15000,'cashew':10000,
    'arecanut':40000,'clove':35000,'cardamom':80000,'pepper':40000,
    'turmeric':7000,'ginger':5000,
    'lucerne':1500,'berseem':1200,'napier_grass':900,'dhaincha':1000,'sunhemp':1000,
    'coriander':7000,'cumin':22000,'ajwain':15000,'fennel':12000,'dill':8000,
    'rose':5000,'marigold':2500,'jasmine':6000,'chrysanthemum':3500,
    'tuberose':4000,'lotus':4000,
    'aloe_vera':800,'ashwagandha':6000,'stevia':8000,'lemongrass':2000,
    'tulsi':2000,'neem':1500,'brahmi':5000,
    'indigo':3000,'tobacco':12000,'hop':20000,'vetiver':5000,
    # aliases
    'potato_veg':800, 'coffee':18000,
}

def _build_features(N, P, K, temperature, humidity, ph, rainfall, crop=None):
    """Build the 13-feature vector. If crop known, use its season/water encoding."""
    NPK_total = N + P + K
    NPK_ratio = N / (P + K + 1)
    heat_idx  = temperature * humidity / 100
    moist_idx = rainfall * humidity / 100
    season_val = _SEASON_ENC.get(crop, 1.0) if crop else 1.0
    water_val  = _WATER_ENC.get(
        CROP_INFO.get(crop, {}).get('water', 'Medium'), 2
    ) if crop else 2.0
    return [N, P, K, temperature, humidity, ph, rainfall,
            season_val, water_val, NPK_total, NPK_ratio, heat_idx, moist_idx]

def _build_features(N, P, K, temperature, humidity, ph, rainfall):
    NP_ratio = min(N / (P + 1), 20)
    KN_ratio = min(K / (N + 1), 10)
    rain_hum = rainfall * humidity / 100
    return np.array([[N, P, K, temperature, humidity, ph, rainfall,
                      NP_ratio, KN_ratio, rain_hum]])

def predict_crop(N, P, K, temperature, humidity, ph, rainfall):
    _load()
    X = _build_features(N, P, K, temperature, humidity, ph, rainfall)
    try:
        X_scaled = _scaler.transform(X)
    except ValueError:
        X_scaled = _scaler.transform(X[:, :7])
    probs = _model.predict_proba(X_scaled)[0]
    top3_idx = np.argsort(probs)[-3:][::-1]
    results = []
    for idx in top3_idx:
        crop = _le.inverse_transform([idx])[0]
        info = CROP_INFO.get(crop, {})
        results.append({
            'crop': crop,
            'confidence': round(probs[idx] * 100, 1),
            'info': info,
            'msp': MANDI_PRICES.get(crop, 0)
        })
    return results

def predict_crop_top20(N, P, K, temperature, humidity, ph, rainfall):
    _load()
    X = _build_features(N, P, K, temperature, humidity, ph, rainfall)
    try:
        X_scaled = _scaler.transform(X)
    except ValueError:
        X_scaled = _scaler.transform(X[:, :7])
    probs = _model.predict_proba(X_scaled)[0]
    top20_idx = np.argsort(probs)[-20:][::-1]
    results = []
    for idx in top20_idx:
        crop = _le.inverse_transform([idx])[0]
        info = CROP_INFO.get(crop, {})
        results.append({
            'crop': crop,
            'confidence': round(probs[idx] * 100, 1),
            'info': info,
            'msp': MANDI_PRICES.get(crop, 0)
        })
    return results

def analyze_soil(ph, moisture):
    tips = []
    health = 'Good'
    if ph < 5.5:
        tips.append("🔴 Soil is too acidic. Apply agricultural lime (CaCO₃) at 2-3 tonnes/hectare.")
        health = 'Poor'
    elif ph < 6.0:
        tips.append("🟡 Slightly acidic. Add wood ash or dolomite lime to raise pH gradually.")
        health = 'Fair'
    elif ph <= 7.0:
        tips.append("🟢 Optimal pH range (6.0-7.0). Suitable for most crops.")
    elif ph <= 7.5:
        tips.append("🟡 Slightly alkaline. Add sulfur or gypsum to lower pH gradually.")
        health = 'Fair'
    else:
        tips.append("🔴 Highly alkaline soil. Apply elemental sulfur and organic matter.")
        health = 'Poor'

    if moisture < 20:
        tips.append("💧 Very dry soil. Increase irrigation frequency. Consider drip irrigation.")
    elif moisture < 40:
        tips.append("💧 Low moisture. Mulching with straw can help retain moisture.")
    elif moisture <= 60:
        tips.append("✅ Optimal moisture level. Maintain with regular irrigation schedule.")
    elif moisture <= 80:
        tips.append("⚠️ High moisture. Ensure proper drainage to prevent root rot.")
    else:
        tips.append("🚨 Waterlogged conditions. Install drainage channels immediately.")

    if ph >= 6.0 and ph <= 7.0 and moisture >= 40 and moisture <= 60:
        tips.append("🌟 Excellent soil conditions! Ideal for high-value vegetable and cash crops.")

    best_crops = []
    checks = [
        ('wheat',    6.0,7.0, 40,70),
        ('rice',     5.5,7.0, 60,80),
        ('maize',    5.8,7.5, 50,70),
        ('cotton',   6.0,7.5, 40,70),
        ('chickpea', 5.5,7.0, 30,60),
        ('mustard',  6.0,7.5, 30,60),
        ('tomato',   6.0,7.0, 50,70),
        ('soybean',  6.0,7.0, 50,70),
    ]
    for crop, plo, phi, mlo, mhi in checks:
        if plo <= ph <= phi and mlo <= moisture <= mhi:
            best_crops.append(crop)

    return {'tips': tips, 'health': health, 'best_crops': best_crops}

# ── Crop Yield Data (tonnes/hectare) from ICAR ────────────────────────────────
CROP_YIELD = {
    'rice':2.5,'wheat':3.2,'maize':2.8,'barley':2.0,'sorghum':1.5,
    'bajra':1.8,'ragi':1.5,'jowar':1.5,'oats':1.8,'triticale':2.5,
    'chickpea':1.0,'kidneybeans':0.8,'pigeonpeas':0.9,'mothbeans':0.6,
    'mungbean':0.8,'blackgram':0.8,'lentil':0.9,'fieldpeas':1.0,
    'cowpea':0.9,'horsegram':0.6,'soybean':1.2,'groundnut':1.5,
    'mustard':1.2,'sunflower':1.2,'sesame':0.5,'linseed':0.7,
    'safflower':0.8,'castor':1.5,'rapeseed':1.2,'cotton':1.8,
    'jute':2.0,'sugarcane':65.0,'sugarbeet':30.0,'sweetpotato':12.0,
    'potato':20.0,'tapioca':25.0,'arrowroot':8.0,'yam':10.0,
    'onion':20.0,'garlic':8.0,'tomato':25.0,'chilli':1.5,'brinjal':20.0,
    'okra':8.0,'peas':6.0,'cabbage':25.0,'cauliflower':20.0,'carrot':15.0,
    'radish':12.0,'spinach':8.0,'fenugreek':1.5,'bitter_gourd':8.0,
    'bottle_gourd':12.0,'ridge_gourd':8.0,'pumpkin':15.0,'cucumber':15.0,
    'pomegranate':12.0,'banana':25.0,'mango':8.0,'grapes':12.0,
    'watermelon':20.0,'muskmelon':12.0,'apple':10.0,'orange':12.0,
    'papaya':30.0,'coconut':10.0,'guava':15.0,'litchi':8.0,
    'jackfruit':10.0,'pineapple':30.0,'strawberry':8.0,'amla':8.0,
    'ber':5.0,'tamarind':3.0,'jamun':5.0,'custard_apple':5.0,
    'sapota':8.0,'fig':5.0,'mulberry':20.0,'coffee':0.8,'tea':2.0,
    'rubber':1.5,'cashew':1.2,'arecanut':2.5,'clove':0.5,
    'cardamom':0.3,'pepper':0.5,'turmeric':6.0,'ginger':15.0,
    'rose':8.0,'marigold':8.0,'jasmine':3.0,'tulsi':3.0,
    'aloe_vera':40.0,'ashwagandha':0.5,'lemongrass':20.0,'stevia':3.0,
    'neem':5.0,'brahmi':8.0,'vetiver':8.0,'indigo':1.5,'tobacco':1.8,
}

def get_yield_estimate(crop, land_area_acres):
    """Estimate yield and income for a crop on given land area."""
    yield_per_ha = CROP_YIELD.get(crop, 2.0)
    ha = land_area_acres * 0.4047
    total_yield_tonnes = yield_per_ha * ha
    total_yield_quintals = total_yield_tonnes * 10
    msp = MANDI_PRICES.get(crop, 2000)
    income = total_yield_quintals * msp
    return {
        'crop': crop,
        'land_acres': land_area_acres,
        'land_ha': round(ha, 2),
        'yield_per_ha': yield_per_ha,
        'total_yield_tonnes': round(total_yield_tonnes, 2),
        'total_yield_quintals': round(total_yield_quintals, 1),
        'msp_per_quintal': msp,
        'estimated_income': round(income, 0),
        'info': CROP_INFO.get(crop, {}),
    }