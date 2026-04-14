"""
Smart-Kissan Translation Module
Primary:  MyMemory API (free, no key, all Indian languages, fast ~200ms)
Fallback: LibreTranslate public instance
Cache:    DB — translate once, serve forever
"""
import logging
import requests as req

logger = logging.getLogger(__name__)

LANGUAGES = {
    'en': {'name': 'English',  'native': 'English',   'lt_code': 'en', 'mm_code': 'en-GB'},
    'hi': {'name': 'Hindi',    'native': 'हिन्दी',     'lt_code': 'hi', 'mm_code': 'hi-IN'},
    'mr': {'name': 'Marathi',  'native': 'मराठी',      'lt_code': 'hi', 'mm_code': 'mr-IN'},
    'te': {'name': 'Telugu',   'native': 'తెలుగు',     'lt_code': 'hi', 'mm_code': 'te-IN'},
    'ta': {'name': 'Tamil',    'native': 'தமிழ்',      'lt_code': 'hi', 'mm_code': 'ta-IN'},
    'kn': {'name': 'Kannada',  'native': 'ಕನ್ನಡ',     'lt_code': 'hi', 'mm_code': 'kn-IN'},
    'pa': {'name': 'Punjabi',  'native': 'ਪੰਜਾਬੀ',     'lt_code': 'hi', 'mm_code': 'pa-IN'},
    'bn': {'name': 'Bengali',  'native': 'বাংলা',      'lt_code': 'bn', 'mm_code': 'bn-IN'},
    'gu': {'name': 'Gujarati', 'native': 'ગુજરાતી',    'lt_code': 'hi', 'mm_code': 'gu-IN'},
    'or': {'name': 'Odia',     'native': 'ଓଡ଼ିଆ',      'lt_code': 'hi', 'mm_code': 'or-IN'},
}

# MyMemory public instances (no key needed)
MYMEMORY_URL = 'https://api.mymemory.translated.net/get'

# LibreTranslate public instances (fallback)
LIBRETRANSLATE_INSTANCES = [
    'https://translate.argosopentech.com',
    'https://libretranslate.de',
    'https://libretranslate.com',
]


def _translate_mymemory(text, lang):
    """MyMemory API - free, no key, ~200ms response."""
    lang_info = LANGUAGES.get(lang, {})
    mm_code = lang_info.get('mm_code', f'{lang}-IN')
    try:
        r = req.get(MYMEMORY_URL, params={
            'q': text[:500],
            'langpair': f'en-GB|{mm_code}',
        }, timeout=6)
        if r.status_code == 200:
            data = r.json()
            translated = data.get('responseData', {}).get('translatedText', '')
            if translated and translated.upper() != text.upper():
                return translated
    except Exception as e:
        logger.debug(f"MyMemory failed: {e}")
    return None


def _translate_libretranslate(text, lang):
    """LibreTranslate fallback."""
    lang_info = LANGUAGES.get(lang, {})
    lt_code = lang_info.get('lt_code', 'hi')
    for instance in LIBRETRANSLATE_INSTANCES:
        try:
            r = req.post(f'{instance}/translate', json={
                'q': text[:500],
                'source': 'en',
                'target': lt_code,
                'format': 'text',
            }, timeout=8)
            if r.status_code == 200:
                translated = r.json().get('translatedText', '')
                if translated and translated != text:
                    return translated
        except Exception:
            continue
    return None


def translate_text(text, lang):
    """
    Translate text with DB caching.
    Order: cache → MyMemory → LibreTranslate → original
    """
    if not text or not text.strip() or lang == 'en':
        return text

    text = text.strip()

    # Check DB cache first
    try:
        from core.models import TranslationCache
        cached = TranslationCache.objects.get(source_text=text[:500], language=lang)
        return cached.translated
    except Exception:
        pass

    # Try MyMemory first (fastest, all Indian languages)
    translated = _translate_mymemory(text, lang)

    # Fallback to LibreTranslate
    if not translated:
        translated = _translate_libretranslate(text, lang)

    # If still nothing, return original
    if not translated:
        return text

    # Save to cache
    try:
        from core.models import TranslationCache
        TranslationCache.objects.get_or_create(
            source_text=text[:500],
            language=lang,
            defaults={'translated': translated}
        )
    except Exception:
        pass

    return translated


def get_lang(request):
    """Get current language from session."""
    lang = request.session.get('lang', 'en')
    if lang not in LANGUAGES:
        lang = 'en'
    return lang


def set_lang(request, lang):
    """Set language in session and user profile."""
    if lang not in LANGUAGES:
        lang = 'en'
    request.session['lang'] = lang
    if request.user.is_authenticated:
        try:
            from core.models import UserProfile
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.language = lang
            profile.save(update_fields=['language'])
        except Exception:
            pass
    return lang