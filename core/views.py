import json
import os
from .translation import translate_text, get_lang, set_lang, LANGUAGES
import io
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import (UserActivity, CropRecommendation, SoilAnalysis,
                     SupportQuery, UserProfile, ChatMessage, YieldEstimate)
from .ml_engine import (predict_crop, analyze_soil, CROP_INFO, MANDI_PRICES,
                        predict_crop_top20, get_yield_estimate, CROP_YIELD)
from .weather import (get_weather, get_soil_by_city, get_regional_crop_bias,
                      get_weather_forecast)


# ── Helpers ──────────────────────────────────────────────────────────────────
def log_activity(user, page, action=''):
    if user.is_authenticated:
        UserActivity.objects.create(user=user, page=page, action=action)


def _get_lang(request):
    return get_lang(request)


# ── TRANSLATIONS (Feature 4: Hindi) ──────────────────────────────────────────
TRANSLATIONS = {
    'hi': {
        'home': 'होम', 'manual': 'मैनुअल', 'auto': 'ऑटो डिटेक्ट',
        'soil_analyzer': 'मृदा विश्लेषक', 'crop_prices': 'फसल मूल्य',
        'all_crops': 'सभी फसलें', 'dashboard': 'डैशबोर्ड', 'support': 'सहायता',
        'welcome': 'स्मार्ट किसान में आपका स्वागत है',
        'recommend': 'फसल सिफारिश करें',
        'detect': 'स्वचालित रूप से पहचानें',
        'current_weather': 'वर्तमान मौसम',
        'quick_stats': 'त्वरित आंकड़े',
        'chat': 'AI सहायक',
        'calendar': 'फसल कैलेंडर',
        'forecast': 'मौसम पूर्वानुमान',
        'yield': 'उपज अनुमानक',
        'mandi': 'मंडी लोकेटर',
    }
}

def get_trans(request, key):
    lang = _get_lang(request)
    if lang == 'hi':
        return TRANSLATIONS['hi'].get(key, key)
    return key


# ── Feature 4: Language toggle ────────────────────────────────────────────────
@login_required
def set_language(request):
    if request.method == 'POST':
        lang = request.POST.get('language', 'en')
        if hasattr(request.user, 'profile'):
            request.user.profile.language = lang
            request.user.profile.save()
        request.session['language'] = lang
    return redirect(request.META.get('HTTP_REFERER', '/'))


# ── LANGUAGE SWITCHING ────────────────────────────────────────────────────────
def switch_language(request):
    """Switch UI language and redirect back."""
    from django.http import HttpResponseRedirect
    lang = request.GET.get('lang', 'en')
    set_lang(request, lang)
    next_url = request.GET.get('next', '/')
    return HttpResponseRedirect(next_url)


def api_translate(request):
    """API endpoint to translate a string on demand — used by JS frontend."""
    from django.http import JsonResponse
    from django.views.decorators.csrf import csrf_exempt

    text = request.GET.get('text', '').strip()
    lang = request.GET.get('lang', 'en')

    if not text or lang == 'en':
        return JsonResponse({'translated': text, 'lang': lang})

    # Only translate meaningful strings
    if len(text) < 2 or text.isdigit():
        return JsonResponse({'translated': text, 'lang': lang})

    translated = translate_text(text, lang)
    return JsonResponse({'translated': translated, 'lang': lang})


# ── HOME ──────────────────────────────────────────────────────────────────────
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    log_activity(request.user, 'home')
    city = (request.user.profile.city
            if hasattr(request.user, 'profile') and request.user.profile.city
            else 'Indore')
    weather = get_weather(city)
    from .ml_engine import CROP_INFO
    return render(request, 'core/home.html', {
        'weather': weather, 'city': city,
        'total_crops': len(CROP_INFO),
        'lang': _get_lang(request),
    })


# ── MANUAL RECOMMEND ─────────────────────────────────────────────────────────
@login_required
def manual_recommend(request):
    log_activity(request.user, 'manual')
    context = {'lang': _get_lang(request)}
    if request.method == 'POST':
        try:
            N    = float(request.POST.get('nitrogen', 0))
            P    = float(request.POST.get('phosphorus', 0))
            K    = float(request.POST.get('potassium', 0))
            temp = float(request.POST.get('temperature', 25))
            hum  = float(request.POST.get('humidity', 60))
            ph   = float(request.POST.get('ph', 7))
            rain = float(request.POST.get('rainfall', 100))
            results = predict_crop(N, P, K, temp, hum, ph, rain)
            top = results[0]
            rec = CropRecommendation.objects.create(
                user=request.user, method='manual', crop_name=top['crop'],
                nitrogen=N, phosphorus=P, potassium=K,
                temperature=temp, humidity=hum, ph=ph, rainfall=rain
            )
            log_activity(request.user, 'manual', f"Recommended: {top['crop']}")
            # Translate tips if needed
            lang = get_lang(request)
            if lang != 'en':
                for r in results:
                    if r.get('tips'):
                        r['tips'] = [translate_text(t, lang) for t in r['tips']]
            context.update({'results': results, 'submitted': True, 'rec_id': rec.id})
        except Exception as e:
            context['error'] = f'Error: {str(e)}'
    return render(request, 'core/manual.html', context)


# ── AUTO RECOMMEND ───────────────────────────────────────────────────────────
@login_required
def auto_recommend(request):
    log_activity(request.user, 'auto')
    context = {'lang': _get_lang(request)}
    if request.method == 'POST':
        city = request.POST.get('city', '').strip()
        if city:
            weather = get_weather(city)
            soil    = get_soil_by_city(city)
            region  = soil.pop('region', 'plains')
            temp    = weather['temp']
            hum     = weather['humidity']
            rain    = weather.get('rainfall', 50) * 10
            N, P, K, ph = soil['N'], soil['P'], soil['K'], soil['ph']

            candidates = predict_crop_top20(N, P, K, temp, hum, ph, rain)
            bias = get_regional_crop_bias(region)
            for r in candidates:
                if r['crop'] in bias['prefer']:
                    r['confidence'] = min(99.0, round(r['confidence'] * 1.5, 1))
                elif r['crop'] in bias['avoid']:
                    r['confidence'] = round(r['confidence'] * 0.3, 1)
            candidates.sort(key=lambda x: x['confidence'], reverse=True)
            results = candidates[:3]
            top = results[0]
            rec = CropRecommendation.objects.create(
                user=request.user, method='auto', crop_name=top['crop'],
                nitrogen=N, phosphorus=P, potassium=K,
                temperature=temp, humidity=hum, ph=ph, rainfall=rain, city=city
            )
            log_activity(request.user, 'auto', f"City:{city}[{region}] → {top['crop']}")
            context.update({
                'results': results, 'weather': weather, 'soil': soil,
                'city': city, 'region': region, 'submitted': True, 'rec_id': rec.id
            })
        else:
            context['error'] = 'Please enter a city name.'
    return render(request, 'core/auto.html', context)


# ── SOIL ANALYZER ────────────────────────────────────────────────────────────
@login_required
def soil_analyzer(request):
    log_activity(request.user, 'soil_analyzer')
    context = {'lang': _get_lang(request)}
    if request.method == 'POST':
        try:
            ph       = float(request.POST.get('ph', 7))
            moisture = float(request.POST.get('moisture', 50))
            result   = analyze_soil(ph, moisture)
            SoilAnalysis.objects.create(
                user=request.user, ph=ph,
                moisture=moisture, tips=str(result)
            )
            log_activity(request.user, 'soil_analyzer', f"pH:{ph}, moisture:{moisture}")
            context.update({
                'result':    result,
                'submitted': True,
                'ph':        ph,
                'moisture':  moisture,
            })
        except Exception as e:
            context['error'] = f'Analysis error: {str(e)}'
    return render(request, 'core/soil_analyzer.html', context)


# ── CROP PRICES ──────────────────────────────────────────────────────────────
@login_required
def crop_prices(request):
    from .weather import get_mandi_prices_live
    import hashlib

    log_activity(request.user, 'crop_prices')

    # ── Tab 1: MSP prices ──────────────────────────────────────
    prices = []
    for crop, msp in sorted(MANDI_PRICES.items(), key=lambda x: -x[1]):
        info = CROP_INFO.get(crop, {})
        seed = int(hashlib.md5(crop.encode()).hexdigest(), 16) % 100
        mandi_est = round(msp * (0.85 + seed / 333), 0)
        prices.append({
            'crop':   crop,
            'msp':    msp,
            'mandi':  mandi_est,
            'diff':   round(mandi_est - msp, 0),
            'season': info.get('season', ''),
            'emoji':  info.get('emoji', '🌱'),
        })

    # ── Tab 2: Live Mandi ──────────────────────────────────────
    tab          = request.GET.get('tab', 'msp')
    mandi_state  = request.GET.get('state', '').lower()
    mandi_crop   = request.GET.get('crop', 'wheat')
    mandi_msp    = MANDI_PRICES.get(mandi_crop, 2000)
    mandi_mandis = []
    mandi_is_live = False

    if tab == 'mandi' and mandi_state:
        live_result = get_mandi_prices_live(mandi_crop, mandi_state)
        if live_result.get('success') and live_result.get('prices'):
            mandi_is_live = True
            for p in live_result['prices'][:10]:
                mandi_mandis.append({
                    'name':        f"{p['market']} Mandi",
                    'city':        p['district'],
                    'state_name':  p['state'],
                    'type':        'APMC',
                    'modal_price': p['modal_price'],
                    'min_price':   p['min_price'],
                    'max_price':   p['max_price'],
                    'date':        p['date'],
                    'variety':     p['variety'],
                    'trend':       '↑' if p['modal_price'] >= mandi_msp else '↓',
                    'lat': 0, 'lng': 0,
                })
        else:
            mandis_raw = list(MAJOR_MANDIS.get(mandi_state, MAJOR_MANDIS['default']))
            for m in mandis_raw:
                seed = int(hashlib.md5(f"{m['name']}{mandi_crop}".encode()).hexdigest(), 16) % 100
                modal = round(mandi_msp * (0.9 + (seed - 50) / 333))
                mandi_mandis.append({
                    **m,
                    'modal_price': modal,
                    'min_price':   round(modal * 0.92),
                    'max_price':   round(modal * 1.08),
                    'trend':       '↑' if seed > 50 else '↓',
                    'date':        'Estimated',
                    'variety':     '—',
                    'state_name':  '',
                })

    all_states = sorted([s for s in MAJOR_MANDIS.keys() if s != 'default'])

    return render(request, 'core/crop_prices.html', {
        'prices':        prices,
        'all_states':    all_states,
        'all_crops':     sorted(MANDI_PRICES.keys()),
        'mandi_state':   mandi_state,
        'mandi_crop':    mandi_crop,
        'mandi_msp':     mandi_msp,
        'mandi_mandis':  mandi_mandis,
        'mandi_is_live': mandi_is_live,
        'lang':          _get_lang(request),
    })


# ── ALL CROPS ────────────────────────────────────────────────────────────────
@login_required
def crops_list(request):
    log_activity(request.user, 'crops_list')
    crops = []
    for crop, info in CROP_INFO.items():
        crops.append({
            'name': crop, 'emoji': info.get('emoji', '🌱'),
            'season': info.get('season', ''), 'water': info.get('water', ''),
            'time': info.get('time', ''), 'msp': MANDI_PRICES.get(crop, 0),
            'tips': info.get('tips', []),
        })
    return render(request, 'core/crops_list.html', {
        'crops': crops, 'lang': _get_lang(request)
    })


# ── DASHBOARD ────────────────────────────────────────────────────────────────
@login_required
def dashboard(request):
    import json
    from collections import Counter
    import datetime

    log_activity(request.user, 'dashboard')
    recs       = CropRecommendation.objects.filter(user=request.user).order_by('-timestamp')
    analyses   = SoilAnalysis.objects.filter(user=request.user)
    activities = UserActivity.objects.filter(user=request.user)

    # Stats
    total_recs       = recs.count()
    total_activities = activities.count()
    manual_count     = recs.filter(method='manual').count()
    auto_count       = recs.filter(method='auto').count()
    soil_analyses    = analyses.count()

    # Weekly activity — last 7 days
    today = datetime.date.today()
    weekly = []
    for i in range(6, -1, -1):
        d = today - datetime.timedelta(days=i)
        count = activities.filter(timestamp__date=d).count()
        weekly.append({'day': d.strftime('%a'), 'count': count})
    weekly_json = json.dumps(weekly)

    # Top crops
    crop_counts = Counter(recs.values_list('crop_name', flat=True))
    crop_json = json.dumps([
        {'crop': k.title(), 'count': v}
        for k, v in crop_counts.most_common(8)
    ])

    # Page distribution
    page_counts = Counter(activities.values_list('page', flat=True))
    page_json = json.dumps([
        {'page': k.title(), 'count': v}
        for k, v in page_counts.most_common(8)
    ])

    return render(request, 'core/dashboard.html', {
        'recs': recs[:20],
        'analyses': analyses,
        'activities': activities[:20],
        'total_recs': total_recs,
        'total_activities': total_activities,
        'manual_count': manual_count,
        'auto_count': auto_count,
        'soil_analyses': soil_analyses,
        'weekly_json': weekly_json,
        'crop_json': crop_json,
        'page_json': page_json,
        'lang': _get_lang(request),
    })


# ── PROFILE ──────────────────────────────────────────────────────────────────
@login_required
def profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name  = request.POST.get('last_name', '')
        request.user.email      = request.POST.get('email', '')
        request.user.save()
        profile.phone     = request.POST.get('phone', '')
        profile.city      = request.POST.get('city', '')
        profile.state     = request.POST.get('state', '')
        profile.farm_size = request.POST.get('farm_size', '')
        profile.bio       = request.POST.get('bio', '')
        profile.language  = request.POST.get('language', 'en')
        if request.FILES.get('avatar'):
            try:
                import cloudinary.uploader
                avatar_file = request.FILES['avatar']
                upload_result = cloudinary.uploader.upload(
                    avatar_file,
                    folder='smart-kissan/avatars',
                    public_id=f'user_{request.user.id}',
                    overwrite=True,
                    resource_type='image',
                    transformation=[
                        {'width': 200, 'height': 200, 'crop': 'fill', 'gravity': 'face'}
                    ]
                )
                # Save Cloudinary URL to profile
                profile.avatar_url = upload_result.get('secure_url', '')
            except Exception as e:
                # Fallback to local storage
                profile.avatar = request.FILES['avatar']
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'core/profile.html', {
        'profile': profile,
        'prof': profile,
        'lang': _get_lang(request),
    })


# ── SUPPORT ──────────────────────────────────────────────────────────────────
@login_required
def support(request):
    if request.method == 'POST':
        SupportQuery.objects.create(
            user=request.user,
            name=request.POST.get('name', ''),
            email=request.POST.get('email', ''),
            subject=request.POST.get('subject', ''),
            message=request.POST.get('message', '')
        )
        messages.success(request, '✅ Message sent! We will respond within 24 hours.')
        return redirect('support')
    return render(request, 'core/support.html', {'lang': _get_lang(request)})


# ── WEATHER API ──────────────────────────────────────────────────────────────
@login_required
def get_weather_api(request):
    city = request.GET.get('city', 'Indore')
    data = get_weather(city)
    return JsonResponse(data)


# ═══════════════════════════════════════════════════════════════════════════════
# ── FEATURE 1: AI CHAT ────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
@login_required
def ai_chat(request):
    log_activity(request.user, 'ai_chat')
    history = ChatMessage.objects.filter(user=request.user).order_by('timestamp')[:50]
    return render(request, 'core/ai_chat.html', {
        'history': history, 'lang': _get_lang(request)
    })


@login_required
@require_POST
def chat_api(request):
    try:
        data    = json.loads(request.body)
        message = data.get('message', '').strip()
        if not message:
            return JsonResponse({'error': 'Empty message'}, status=400)

        # Save user message
        ChatMessage.objects.create(user=request.user, role='user', content=message)

        # Build conversation history
        history = list(ChatMessage.objects.filter(
            user=request.user).order_by('timestamp')[:20].values('role', 'content'))

        lang = _get_lang(request)
        system_prompt = (
            "You are Smart-Kissan AI, an expert agricultural assistant for Indian farmers. "
            "You help with crop recommendations, farming techniques, pest control, soil health, "
            "weather advice, MSP prices, and government schemes for farmers. "
            + ("Respond in Hindi (Devanagari script)." if lang == 'hi' else "Respond in simple, clear English.")
            + " Keep responses concise and practical. Use bullet points for tips. "
            "Always consider Indian farming context, seasons (Kharif/Rabi/Zaid), and local conditions."
        )

        # Build conversation history for Groq
        from groq import Groq
        client = Groq(api_key=os.environ.get('GROQ_API_KEY', ''))

        msgs = [{'role': 'system', 'content': system_prompt}]
        for m in list(history)[:-1]:
            msgs.append({'role': m['role'], 'content': m['content']})
        msgs.append({'role': 'user', 'content': message})

        response = client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=msgs,
            max_tokens=600,
            temperature=0.7,
        )
        reply = response.choices[0].message.content

        # Save assistant reply
        ChatMessage.objects.create(user=request.user, role='assistant', content=reply)
        return JsonResponse({'reply': reply})

    except Exception as e:
        err = str(e)
        if '429' in err or 'rate_limit' in err.lower():
            fallback = 'Rate limit reached. Please wait a moment and try again.'
        elif 'api_key' in err.lower() or 'authentication' in err.lower():
            fallback = 'Invalid Groq API key. Please check GROQ_API_KEY in settings.py.'
        elif 'model' in err.lower() and ('not found' in err.lower() or '404' in err):
            fallback = 'Model unavailable. Please try again in a moment.'
        else:
            fallback = f'AI error: {err[:120]}'
        ChatMessage.objects.create(user=request.user, role='assistant', content=fallback)
        return JsonResponse({'reply': fallback})


# ═══════════════════════════════════════════════════════════════════════════════
# ── FEATURE 2: CROP CALENDAR ──────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
CROP_CALENDAR_DATA = {
    # Kharif crops (June-November)
    'rice':       {'sow':['Jun','Jul'],'grow':['Aug','Sep','Oct'],'harvest':['Oct','Nov'],'season':'Kharif'},
    'maize':      {'sow':['Jun','Jul'],'grow':['Aug','Sep'],'harvest':['Sep','Oct'],'season':'Kharif'},
    'cotton':     {'sow':['May','Jun'],'grow':['Jul','Aug','Sep','Oct'],'harvest':['Nov','Dec'],'season':'Kharif'},
    'sugarcane':  {'sow':['Feb','Mar'],'grow':['Apr','May','Jun','Jul','Aug','Sep','Oct','Nov'],'harvest':['Dec','Jan','Feb'],'season':'Kharif'},
    'soybean':    {'sow':['Jun','Jul'],'grow':['Aug','Sep'],'harvest':['Oct','Nov'],'season':'Kharif'},
    'groundnut':  {'sow':['Jun','Jul'],'grow':['Aug','Sep'],'harvest':['Oct','Nov'],'season':'Kharif'},
    'bajra':      {'sow':['Jul','Aug'],'grow':['Aug','Sep'],'harvest':['Oct','Nov'],'season':'Kharif'},
    'jowar':      {'sow':['Jun','Jul'],'grow':['Aug','Sep'],'harvest':['Sep','Oct'],'season':'Kharif'},
    'jute':       {'sow':['Mar','Apr'],'grow':['May','Jun','Jul'],'harvest':['Aug','Sep'],'season':'Kharif'},
    'turmeric':   {'sow':['Jun','Jul'],'grow':['Aug','Sep','Oct','Nov','Dec'],'harvest':['Jan','Feb','Mar'],'season':'Kharif'},
    'ginger':     {'sow':['Apr','May'],'grow':['Jun','Jul','Aug','Sep'],'harvest':['Dec','Jan','Feb'],'season':'Kharif'},
    'banana':     {'sow':['Jun','Jul'],'grow':['Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr'],'harvest':['May','Jun','Jul'],'season':'Kharif'},
    'tomato':     {'sow':['Jun','Jul'],'grow':['Aug','Sep'],'harvest':['Oct','Nov'],'season':'Kharif'},
    'okra':       {'sow':['Jun','Jul'],'grow':['Aug'],'harvest':['Sep','Oct'],'season':'Kharif'},
    'chilli':     {'sow':['Jun','Jul'],'grow':['Aug','Sep','Oct'],'harvest':['Nov','Dec'],'season':'Kharif'},
    'brinjal':    {'sow':['Jun','Jul'],'grow':['Aug','Sep','Oct'],'harvest':['Nov','Dec'],'season':'Kharif'},
    # Rabi crops (November-April)
    'wheat':      {'sow':['Nov','Dec'],'grow':['Jan','Feb'],'harvest':['Mar','Apr'],'season':'Rabi'},
    'mustard':    {'sow':['Oct','Nov'],'grow':['Dec','Jan'],'harvest':['Feb','Mar'],'season':'Rabi'},
    'chickpea':   {'sow':['Oct','Nov'],'grow':['Dec','Jan'],'harvest':['Feb','Mar'],'season':'Rabi'},
    'lentil':     {'sow':['Oct','Nov'],'grow':['Dec','Jan'],'harvest':['Feb','Mar'],'season':'Rabi'},
    'potato':     {'sow':['Oct','Nov'],'grow':['Dec','Jan'],'harvest':['Feb','Mar'],'season':'Rabi'},
    'onion':      {'sow':['Oct','Nov'],'grow':['Dec','Jan','Feb'],'harvest':['Mar','Apr'],'season':'Rabi'},
    'garlic':     {'sow':['Oct','Nov'],'grow':['Dec','Jan'],'harvest':['Feb','Mar'],'season':'Rabi'},
    'peas':       {'sow':['Oct','Nov'],'grow':['Dec','Jan'],'harvest':['Feb','Mar'],'season':'Rabi'},
    'barley':     {'sow':['Nov','Dec'],'grow':['Jan','Feb'],'harvest':['Mar','Apr'],'season':'Rabi'},
    'coriander':  {'sow':['Oct','Nov'],'grow':['Dec','Jan'],'harvest':['Feb','Mar'],'season':'Rabi'},
    'cumin':      {'sow':['Nov','Dec'],'grow':['Jan','Feb'],'harvest':['Feb','Mar'],'season':'Rabi'},
    'carrot':     {'sow':['Oct','Nov'],'grow':['Dec','Jan'],'harvest':['Feb','Mar'],'season':'Rabi'},
    'spinach':    {'sow':['Oct','Nov'],'grow':['Dec','Jan'],'harvest':['Feb','Mar'],'season':'Rabi'},
    'cabbage':    {'sow':['Oct','Nov'],'grow':['Dec','Jan'],'harvest':['Feb','Mar'],'season':'Rabi'},
    'cauliflower':{'sow':['Oct','Nov'],'grow':['Dec','Jan'],'harvest':['Feb','Mar'],'season':'Rabi'},
    'sunflower':  {'sow':['Nov','Dec'],'grow':['Jan','Feb'],'harvest':['Mar','Apr'],'season':'Rabi'},
    # Zaid crops (March-June)
    'watermelon': {'sow':['Feb','Mar'],'grow':['Apr'],'harvest':['May','Jun'],'season':'Zaid'},
    'muskmelon':  {'sow':['Feb','Mar'],'grow':['Apr'],'harvest':['May','Jun'],'season':'Zaid'},
    'cucumber':   {'sow':['Feb','Mar'],'grow':['Apr'],'harvest':['May','Jun'],'season':'Zaid'},
    'mungbean':   {'sow':['Mar','Apr'],'grow':['May'],'harvest':['Jun','Jul'],'season':'Zaid'},
    'cowpea':     {'sow':['Mar','Apr'],'grow':['May'],'harvest':['Jun','Jul'],'season':'Zaid'},
    'bitter_gourd':{'sow':['Feb','Mar'],'grow':['Apr','May'],'harvest':['May','Jun'],'season':'Zaid'},
    'bottle_gourd':{'sow':['Feb','Mar'],'grow':['Apr','May'],'harvest':['May','Jun'],'season':'Zaid'},
    'radish':     {'sow':['Mar','Apr'],'grow':['Apr','May'],'harvest':['May','Jun'],'season':'Zaid'},
    # Perennial
    'coconut':    {'sow':['Jun','Jul'],'grow':['Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr'],'harvest':['All year'],'season':'Zaid'},
    'mango':      {'sow':['Jun','Jul'],'grow':['Aug','Sep','Oct','Nov','Dec','Jan'],'harvest':['Apr','May','Jun'],'season':'Zaid'},
    'papaya':     {'sow':['Jun','Jul'],'grow':['Aug','Sep','Oct','Nov','Dec'],'harvest':['Jan','Feb','Mar'],'season':'Zaid'},
    'coffee':     {'sow':['Jun','Jul'],'grow':['Aug','Sep','Oct','Nov'],'harvest':['Dec','Jan','Feb'],'season':'Zaid'},
    'tea':        {'sow':['Mar','Apr'],'grow':['May','Jun','Jul','Aug'],'harvest':['Sep','Oct','Nov'],'season':'Zaid'},
    'rubber':     {'sow':['Jun','Jul'],'grow':['Aug','Sep','Oct','Nov','Dec'],'harvest':['Jan','Feb','Mar'],'season':'Zaid'},
}

@login_required
def crop_calendar(request):
    log_activity(request.user, 'crop_calendar')
    import datetime
    current_month = datetime.date.today().strftime('%b')
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    selected_crop = request.GET.get('crop', '')
    selected_season = request.GET.get('season', 'all')

    calendar_data = {}
    for crop, data in CROP_CALENDAR_DATA.items():
        if selected_season != 'all' and data['season'] != selected_season:
            continue
        calendar_data[crop] = data

    crop_detail = CROP_CALENDAR_DATA.get(selected_crop, {})

    # Which crops are active THIS month
    active_now = []
    for crop, data in CROP_CALENDAR_DATA.items():
        status = ''
        if current_month in data.get('sow', []):
            status = 'sow'
        elif current_month in data.get('grow', []):
            status = 'grow'
        elif current_month in data.get('harvest', []):
            status = 'harvest'
        if status:
            active_now.append({'crop': crop, 'status': status,
                                'season': data['season'],
                                'emoji': CROP_INFO.get(crop, {}).get('emoji', '🌱')})

    return render(request, 'core/crop_calendar.html', {
        'calendar_data': calendar_data,
        'months': months,
        'current_month': current_month,
        'active_now': active_now,
        'selected_crop': selected_crop,
        'crop_detail': crop_detail,
        'selected_season': selected_season,
        'all_crops': sorted(CROP_CALENDAR_DATA.keys()),
        'lang': _get_lang(request),
    })


# ═══════════════════════════════════════════════════════════════════════════════
# ── FEATURE 5: 7-DAY WEATHER FORECAST ────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
@login_required
def weather_forecast(request):
    log_activity(request.user, 'weather_forecast')
    city = request.GET.get('city', '')
    if not city and hasattr(request.user, 'profile'):
        city = request.user.profile.city or 'Indore'
    if not city:
        city = 'Indore'
    forecast_data = get_weather_forecast(city)
    current = get_weather(city)
    return render(request, 'core/weather_forecast.html', {
        'forecast': forecast_data,
        'current': current,
        'city': city,
        'lang': _get_lang(request),
    })


# ═══════════════════════════════════════════════════════════════════════════════
# ── FEATURE 6: YIELD ESTIMATOR ────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
@login_required
def yield_estimator(request):
    log_activity(request.user, 'yield_estimator')
    context = {'crops': sorted(CROP_INFO.keys()), 'lang': _get_lang(request)}
    if request.method == 'POST':
        crop      = request.POST.get('crop', '')
        area      = float(request.POST.get('area', 1))
        area_unit = request.POST.get('area_unit', 'acres')
        if area_unit == 'hectares':
            area_acres = area * 2.471
        elif area_unit == 'bigha':
            area_acres = area * 0.619
        else:
            area_acres = area
        result = get_yield_estimate(crop, area_acres)
        result['input_area'] = area
        result['area_unit']  = area_unit
        YieldEstimate.objects.create(
            user=request.user, crop=crop,
            land_area=area_acres, area_unit=area_unit,
            estimated_yield=result['total_yield_quintals'],
            estimated_income=result['estimated_income'],
            msp_price=result['msp_per_quintal']
        )
        log_activity(request.user, 'yield_estimator', f"{crop} {area}{area_unit}")
        # Calculate income scenarios
        income     = result['estimated_income']
        qtl        = result['total_yield_quintals']
        msp        = result['msp_per_quintal']
        result['income_low']       = round(qtl * 0.7 * msp)
        result['income_high']      = round(qtl * 1.3 * msp)
        result['yield_low']        = round(qtl * 0.7, 1)
        result['yield_high']       = round(qtl * 1.3, 1)
        context['result'] = result
    return render(request, 'core/yield_estimator.html', context)


# ═══════════════════════════════════════════════════════════════════════════════
# ── FEATURE 7: MANDI LOCATOR ──────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
MAJOR_MANDIS = {
    'madhya pradesh': [
        {'name':'Indore Mandi',   'city':'Indore',   'lat':22.7196,'lng':75.8577,'type':'APMC'},
        {'name':'Bhopal Mandi',   'city':'Bhopal',   'lat':23.2599,'lng':77.4126,'type':'APMC'},
        {'name':'Gwalior Mandi',  'city':'Gwalior',  'lat':26.2183,'lng':78.1828,'type':'APMC'},
        {'name':'Jabalpur Mandi', 'city':'Jabalpur', 'lat':23.1815,'lng':79.9864,'type':'APMC'},
        {'name':'Ujjain Mandi',   'city':'Ujjain',   'lat':23.1765,'lng':75.7885,'type':'APMC'},
        {'name':'Sagar Mandi',    'city':'Sagar',    'lat':23.8388,'lng':78.7378,'type':'APMC'},
        {'name':'Rewa Mandi',     'city':'Rewa',     'lat':24.5362,'lng':81.2964,'type':'APMC'},
    ],
    'maharashtra': [
        {'name':'Pune APMC',        'city':'Pune',       'lat':18.5204,'lng':73.8567,'type':'APMC'},
        {'name':'Nashik Mandi',     'city':'Nashik',     'lat':20.0059,'lng':73.7794,'type':'APMC'},
        {'name':'Nagpur Mandi',     'city':'Nagpur',     'lat':21.1458,'lng':79.0882,'type':'APMC'},
        {'name':'Aurangabad Mandi', 'city':'Aurangabad', 'lat':19.8762,'lng':75.3433,'type':'APMC'},
        {'name':'Solapur Mandi',    'city':'Solapur',    'lat':17.6805,'lng':75.9064,'type':'APMC'},
        {'name':'Kolhapur Mandi',   'city':'Kolhapur',   'lat':16.7050,'lng':74.2433,'type':'APMC'},
    ],
    'punjab': [
        {'name':'Amritsar Grain Market','city':'Amritsar', 'lat':31.6340,'lng':74.8723,'type':'Grain'},
        {'name':'Ludhiana Mandi',       'city':'Ludhiana', 'lat':30.9010,'lng':75.8573,'type':'APMC'},
        {'name':'Patiala Mandi',        'city':'Patiala',  'lat':30.3398,'lng':76.3869,'type':'APMC'},
        {'name':'Jalandhar Mandi',      'city':'Jalandhar','lat':31.3260,'lng':75.5762,'type':'APMC'},
        {'name':'Bathinda Mandi',       'city':'Bathinda', 'lat':30.2110,'lng':74.9455,'type':'Grain'},
    ],
    'uttar pradesh': [
        {'name':'Lucknow Mandi',   'city':'Lucknow',   'lat':26.8467,'lng':80.9462,'type':'APMC'},
        {'name':'Agra Mandi',      'city':'Agra',      'lat':27.1767,'lng':78.0081,'type':'APMC'},
        {'name':'Kanpur Mandi',    'city':'Kanpur',    'lat':26.4499,'lng':80.3319,'type':'APMC'},
        {'name':'Varanasi Mandi',  'city':'Varanasi',  'lat':25.3176,'lng':82.9739,'type':'APMC'},
        {'name':'Meerut Mandi',    'city':'Meerut',    'lat':28.9845,'lng':77.7064,'type':'APMC'},
        {'name':'Allahabad Mandi', 'city':'Allahabad', 'lat':25.4358,'lng':81.8463,'type':'APMC'},
    ],
    'rajasthan': [
        {'name':'Jaipur Mandi',  'city':'Jaipur',  'lat':26.9124,'lng':75.7873,'type':'APMC'},
        {'name':'Jodhpur Mandi', 'city':'Jodhpur', 'lat':26.2389,'lng':73.0243,'type':'APMC'},
        {'name':'Kota Mandi',    'city':'Kota',    'lat':25.2138,'lng':75.8648,'type':'APMC'},
        {'name':'Udaipur Mandi', 'city':'Udaipur', 'lat':24.5854,'lng':73.7125,'type':'APMC'},
        {'name':'Bikaner Mandi', 'city':'Bikaner', 'lat':28.0229,'lng':73.3119,'type':'APMC'},
        {'name':'Ajmer Mandi',   'city':'Ajmer',   'lat':26.4499,'lng':74.6399,'type':'APMC'},
    ],
    'haryana': [
        {'name':'Karnal Mandi',    'city':'Karnal',    'lat':29.6857,'lng':76.9905,'type':'Grain'},
        {'name':'Hisar Mandi',     'city':'Hisar',     'lat':29.1492,'lng':75.7217,'type':'APMC'},
        {'name':'Ambala Mandi',    'city':'Ambala',    'lat':30.3752,'lng':76.7821,'type':'Grain'},
        {'name':'Rohtak Mandi',    'city':'Rohtak',    'lat':28.8955,'lng':76.6066,'type':'APMC'},
        {'name':'Gurugram Mandi',  'city':'Gurugram',  'lat':28.4595,'lng':77.0266,'type':'APMC'},
    ],
    'gujarat': [
        {'name':'Ahmedabad APMC', 'city':'Ahmedabad','lat':23.0225,'lng':72.5714,'type':'APMC'},
        {'name':'Surat Mandi',    'city':'Surat',    'lat':21.1702,'lng':72.8311,'type':'APMC'},
        {'name':'Rajkot Mandi',   'city':'Rajkot',   'lat':22.3039,'lng':70.8022,'type':'APMC'},
        {'name':'Vadodara Mandi', 'city':'Vadodara', 'lat':22.3072,'lng':73.1812,'type':'APMC'},
        {'name':'Junagadh Mandi', 'city':'Junagadh', 'lat':21.5222,'lng':70.4579,'type':'APMC'},
    ],
    'bihar': [
        {'name':'Patna Mandi',    'city':'Patna',    'lat':25.5941,'lng':85.1376,'type':'APMC'},
        {'name':'Muzaffarpur Mandi','city':'Muzaffarpur','lat':26.1209,'lng':85.3647,'type':'APMC'},
        {'name':'Gaya Mandi',     'city':'Gaya',     'lat':24.7955,'lng':84.9994,'type':'APMC'},
        {'name':'Darbhanga Mandi','city':'Darbhanga','lat':26.1542,'lng':85.8918,'type':'APMC'},
    ],
    'west bengal': [
        {'name':'Kolkata Kolay Market','city':'Kolkata',    'lat':22.5726,'lng':88.3639,'type':'APMC'},
        {'name':'Howrah Mandi',        'city':'Howrah',     'lat':22.5958,'lng':88.2636,'type':'APMC'},
        {'name':'Siliguri Mandi',      'city':'Siliguri',   'lat':26.7271,'lng':88.3953,'type':'APMC'},
        {'name':'Burdwan Mandi',       'city':'Burdwan',    'lat':23.2324,'lng':87.8615,'type':'APMC'},
    ],
    'karnataka': [
        {'name':'Bangalore APMC',   'city':'Bangalore', 'lat':12.9716,'lng':77.5946,'type':'APMC'},
        {'name':'Hubli Mandi',      'city':'Hubli',     'lat':15.3647,'lng':75.1240,'type':'APMC'},
        {'name':'Mysore Mandi',     'city':'Mysore',    'lat':12.2958,'lng':76.6394,'type':'APMC'},
        {'name':'Belgaum Mandi',    'city':'Belgaum',   'lat':15.8497,'lng':74.4977,'type':'APMC'},
        {'name':'Mangalore Mandi',  'city':'Mangalore', 'lat':12.9141,'lng':74.8560,'type':'APMC'},
    ],
    'andhra pradesh': [
        {'name':'Vijayawada Mandi',    'city':'Vijayawada',    'lat':16.5062,'lng':80.6480,'type':'APMC'},
        {'name':'Visakhapatnam Mandi', 'city':'Visakhapatnam', 'lat':17.6868,'lng':83.2185,'type':'APMC'},
        {'name':'Guntur Mandi',        'city':'Guntur',        'lat':16.3067,'lng':80.4365,'type':'APMC'},
        {'name':'Tirupati Mandi',      'city':'Tirupati',      'lat':13.6288,'lng':79.4192,'type':'APMC'},
    ],
    'telangana': [
        {'name':'Hyderabad Mandi',  'city':'Hyderabad', 'lat':17.3850,'lng':78.4867,'type':'APMC'},
        {'name':'Warangal Mandi',   'city':'Warangal',  'lat':17.9784,'lng':79.5941,'type':'APMC'},
        {'name':'Nizamabad Mandi',  'city':'Nizamabad', 'lat':18.6725,'lng':78.0941,'type':'APMC'},
        {'name':'Karimnagar Mandi', 'city':'Karimnagar','lat':18.4386,'lng':79.1288,'type':'APMC'},
    ],
    'tamil nadu': [
        {'name':'Chennai Koyambedu','city':'Chennai',    'lat':13.0732,'lng':80.2109,'type':'APMC'},
        {'name':'Coimbatore Mandi', 'city':'Coimbatore','lat':11.0168,'lng':76.9558,'type':'APMC'},
        {'name':'Madurai Mandi',    'city':'Madurai',   'lat':9.9252,'lng':78.1198,'type':'APMC'},
        {'name':'Salem Mandi',      'city':'Salem',     'lat':11.6643,'lng':78.1460,'type':'APMC'},
        {'name':'Trichy Mandi',     'city':'Trichy',    'lat':10.7905,'lng':78.7047,'type':'APMC'},
    ],
    'kerala': [
        {'name':'Ernakulam Mandi',       'city':'Ernakulam',      'lat':9.9816,'lng':76.2999,'type':'APMC'},
        {'name':'Thiruvananthapuram Mandi','city':'Thiruvananthapuram','lat':8.5241,'lng':76.9366,'type':'APMC'},
        {'name':'Kozhikode Mandi',       'city':'Kozhikode',      'lat':11.2588,'lng':75.7804,'type':'APMC'},
        {'name':'Thrissur Mandi',        'city':'Thrissur',       'lat':10.5276,'lng':76.2144,'type':'APMC'},
    ],
    'odisha': [
        {'name':'Bhubaneswar Mandi','city':'Bhubaneswar','lat':20.2961,'lng':85.8245,'type':'APMC'},
        {'name':'Cuttack Mandi',    'city':'Cuttack',    'lat':20.4625,'lng':85.8830,'type':'APMC'},
        {'name':'Sambalpur Mandi',  'city':'Sambalpur',  'lat':21.4669,'lng':83.9756,'type':'APMC'},
    ],
    'jharkhand': [
        {'name':'Ranchi Mandi',  'city':'Ranchi',  'lat':23.3441,'lng':85.3096,'type':'APMC'},
        {'name':'Jamshedpur Mandi','city':'Jamshedpur','lat':22.8046,'lng':86.2029,'type':'APMC'},
        {'name':'Dhanbad Mandi', 'city':'Dhanbad', 'lat':23.7957,'lng':86.4304,'type':'APMC'},
    ],
    'chhattisgarh': [
        {'name':'Raipur Mandi',  'city':'Raipur',  'lat':21.2514,'lng':81.6296,'type':'APMC'},
        {'name':'Bilaspur Mandi','city':'Bilaspur','lat':22.0797,'lng':82.1409,'type':'APMC'},
        {'name':'Durg Mandi',    'city':'Durg',    'lat':21.1904,'lng':81.2849,'type':'APMC'},
    ],
    'himachal pradesh': [
        {'name':'Shimla Mandi',  'city':'Shimla',  'lat':31.1048,'lng':77.1734,'type':'APMC'},
        {'name':'Solan Mandi',   'city':'Solan',   'lat':30.9045,'lng':77.0967,'type':'APMC'},
        {'name':'Kullu Mandi',   'city':'Kullu',   'lat':31.9579,'lng':77.1095,'type':'APMC'},
    ],
    'uttarakhand': [
        {'name':'Dehradun Mandi', 'city':'Dehradun', 'lat':30.3165,'lng':78.0322,'type':'APMC'},
        {'name':'Haridwar Mandi', 'city':'Haridwar', 'lat':29.9457,'lng':78.1642,'type':'APMC'},
        {'name':'Haldwani Mandi', 'city':'Haldwani', 'lat':29.2183,'lng':79.5130,'type':'APMC'},
    ],
    'assam': [
        {'name':'Guwahati Mandi','city':'Guwahati','lat':26.1445,'lng':91.7362,'type':'APMC'},
        {'name':'Silchar Mandi', 'city':'Silchar', 'lat':24.8333,'lng':92.7789,'type':'APMC'},
        {'name':'Dibrugarh Mandi','city':'Dibrugarh','lat':27.4728,'lng':94.9120,'type':'APMC'},
    ],
    'delhi': [
        {'name':'Azadpur Mandi',  'city':'Delhi','lat':28.7238,'lng':77.1745,'type':'APMC'},
        {'name':'Okhla Mandi',    'city':'Delhi','lat':28.5355,'lng':77.2700,'type':'APMC'},
        {'name':'Shahdara Mandi', 'city':'Delhi','lat':28.6692,'lng':77.2888,'type':'APMC'},
        {'name':'Keshopur Mandi', 'city':'Delhi','lat':28.6562,'lng':77.0773,'type':'APMC'},
    ],
    'default': [
        {'name':'Delhi Azadpur Mandi','city':'Delhi',     'lat':28.7238,'lng':77.1745,'type':'APMC'},
        {'name':'Bangalore APMC',     'city':'Bangalore', 'lat':12.9716,'lng':77.5946,'type':'APMC'},
        {'name':'Chennai Koyambedu',  'city':'Chennai',   'lat':13.0732,'lng':80.2109,'type':'APMC'},
        {'name':'Mumbai APMC Vashi',  'city':'Mumbai',    'lat':19.0728,'lng':73.0183,'type':'APMC'},
        {'name':'Hyderabad Mandi',    'city':'Hyderabad', 'lat':17.3850,'lng':78.4867,'type':'APMC'},
    ]
}

@login_required
def mandi_locator(request):
    from .weather import get_mandi_prices_live
    import hashlib

    log_activity(request.user, 'mandi_locator')
    city          = request.GET.get('city', '')
    state         = request.GET.get('state', '').lower()
    selected_crop = request.GET.get('crop', 'wheat')

    if not state and hasattr(request.user, 'profile'):
        city  = request.user.profile.city  or city
        state = (request.user.profile.state or '').lower()

    if not state:
        state = 'madhya pradesh'

    msp = MANDI_PRICES.get(selected_crop, 2000)

    # Try live API first
    live_result = get_mandi_prices_live(selected_crop, state)
    live_prices = []
    is_live     = False

    if live_result.get('success') and live_result.get('prices'):
        is_live     = True
        live_prices = live_result['prices']
        # Format for template compatibility
        mandis = []
        for p in live_prices[:10]:
            mandis.append({
                'name':        f"{p['market']} Mandi",
                'city':        p['district'],
                'state_name':  p['state'],
                'type':        'APMC',
                'modal_price': p['modal_price'],
                'min_price':   p['min_price'],
                'max_price':   p['max_price'],
                'date':        p['date'],
                'variety':     p['variety'],
                'trend':       '↑' if p['modal_price'] >= msp else '↓',
                'lat': 0, 'lng': 0,
            })
    else:
        # Fallback to hardcoded mandis with estimated prices
        mandis = list(MAJOR_MANDIS.get(state, MAJOR_MANDIS['default']))
        for m in mandis:
            seed = int(hashlib.md5(f"{m['name']}{selected_crop}".encode()).hexdigest(), 16) % 100
            variation = (seed - 50) / 100
            m['modal_price'] = round(msp * (0.9 + variation * 0.3))
            m['min_price']   = round(m['modal_price'] * 0.92)
            m['max_price']   = round(m['modal_price'] * 1.08)
            m['trend']       = '↑' if seed > 50 else '↓'
            m['date']        = 'Estimated'
            m['variety']     = '—'

    all_states = sorted([s for s in MAJOR_MANDIS.keys() if s != 'default'])

    return render(request, 'core/mandi_locator.html', {
        'mandis':        mandis,
        'city':          city,
        'state':         state,
        'selected_crop': selected_crop,
        'crops':         sorted(MANDI_PRICES.keys()),
        'msp':           msp,
        'is_live':       is_live,
        'lang':          _get_lang(request),
        'all_states':    all_states,
        'mandi_count':   len(mandis),
        'api_error':     live_result.get('error', '') if not is_live else '',
    })


# ═══════════════════════════════════════════════════════════════════════════════
# ── FEATURE 9: PDF EXPORT ─────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
@login_required
def export_recommendation_pdf(request, rec_id):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle, HRFlowable)
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    import datetime

    rec = get_object_or_404(CropRecommendation, id=rec_id, user=request.user)
    info = CROP_INFO.get(rec.crop_name, {})
    tips = info.get('tips', [])
    msp  = MANDI_PRICES.get(rec.crop_name, 0)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    green  = colors.HexColor('#1a7a3e')
    amber  = colors.HexColor('#d97706')
    dark   = colors.HexColor('#111827')
    light  = colors.HexColor('#f0f9f4')

    title_style   = ParagraphStyle('title',   fontSize=22, textColor=green,
                                   fontName='Helvetica-Bold', alignment=TA_CENTER,
                                   spaceAfter=4)
    sub_style     = ParagraphStyle('sub',     fontSize=11, textColor=colors.grey,
                                   alignment=TA_CENTER, spaceAfter=20)
    heading_style = ParagraphStyle('heading', fontSize=13, textColor=green,
                                   fontName='Helvetica-Bold', spaceAfter=8, spaceBefore=14)
    body_style    = ParagraphStyle('body',    fontSize=10, textColor=dark,
                                   leading=16, spaceAfter=6)
    tip_style     = ParagraphStyle('tip',     fontSize=10, textColor=dark,
                                   leading=15, leftIndent=12)

    story = []
    story.append(Paragraph('🌾 Smart-Kissan', title_style))
    story.append(Paragraph('AI Crop Recommendation Report', sub_style))
    story.append(HRFlowable(width='100%', thickness=2, color=green))
    story.append(Spacer(1, 14))

    story.append(Paragraph(f'Recommended Crop: {rec.crop_name.title()}', heading_style))

    # Crop summary table
    crop_data = [
        ['Season', info.get('season','—')],
        ['Water Need', info.get('water','—')],
        ['Duration', info.get('time','—')],
        ['MSP Price', f'₹{msp:,}/quintal'],
        ['Method', rec.method.title()],
    ]
    if rec.city:
        crop_data.append(['City', rec.city.title()])
    t = Table(crop_data, colWidths=[5*cm, 11*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), light),
        ('TEXTCOLOR',  (0,0), (0,-1), green),
        ('FONTNAME',   (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS',(0,0),(-1,-1),[colors.white, light]),
        ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor('#d1fae5')),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING',(0,0),(-1,-1), 7),
        ('LEFTPADDING',(0,0), (-1,-1), 10),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))

    # Soil/Weather inputs
    story.append(Paragraph('Input Parameters', heading_style))
    params = []
    if rec.nitrogen    is not None: params.append(['Nitrogen (N)',    f'{rec.nitrogen} kg/ha'])
    if rec.phosphorus  is not None: params.append(['Phosphorus (P)',  f'{rec.phosphorus} kg/ha'])
    if rec.potassium   is not None: params.append(['Potassium (K)',   f'{rec.potassium} kg/ha'])
    if rec.temperature is not None: params.append(['Temperature',     f'{rec.temperature}°C'])
    if rec.humidity    is not None: params.append(['Humidity',        f'{rec.humidity}%'])
    if rec.ph          is not None: params.append(['Soil pH',         str(rec.ph)])
    if rec.rainfall    is not None: params.append(['Rainfall',        f'{rec.rainfall} mm'])
    if params:
        t2 = Table(params, colWidths=[5*cm, 11*cm])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#fefce8')),
            ('TEXTCOLOR',  (0,0), (0,-1), amber),
            ('FONTNAME',   (0,0), (0,-1), 'Helvetica-Bold'),
            ('FONTSIZE',   (0,0), (-1,-1), 10),
            ('ROWBACKGROUNDS',(0,0),(-1,-1),[colors.white, colors.HexColor('#fefce8')]),
            ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor('#fde68a')),
            ('TOPPADDING', (0,0), (-1,-1), 7),
            ('BOTTOMPADDING',(0,0),(-1,-1), 7),
            ('LEFTPADDING',(0,0), (-1,-1), 10),
        ]))
        story.append(t2)
        story.append(Spacer(1, 14))

    # Farming tips
    if tips:
        story.append(Paragraph('💡 Farming Tips', heading_style))
        for i, tip in enumerate(tips[:6], 1):
            story.append(Paragraph(f'{i}. {tip}', tip_style))
        story.append(Spacer(1, 10))

    # Footer
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#d1fae5')))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        f'Generated by Smart-Kissan AI | {datetime.datetime.now().strftime("%d %b %Y %I:%M %p")} | '
        f'User: {request.user.get_full_name() or request.user.username}',
        ParagraphStyle('footer', fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
    ))

    doc.build(story)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="SmartKissan_{rec.crop_name}_{rec.id}.pdf"')
    return response


# ═══════════════════════════════════════════════════════════════════════════════
# ── FEATURE 11: FEEDBACK ──────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════
@login_required
@require_POST
def submit_feedback(request):
    try:
        data     = json.loads(request.body)
        rec_id   = data.get('rec_id')
        feedback = data.get('feedback')  # 'helpful' or 'not_helpful'
        if rec_id and feedback:
            rec = CropRecommendation.objects.filter(id=rec_id, user=request.user).first()
            if rec:
                rec.feedback = feedback
                rec.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)