from .translation import get_lang, LANGUAGES

def lang_context(request):
    """Inject language info into every template."""
    current_lang = get_lang(request)
    return {
        'current_lang': current_lang,
        'current_lang_name': LANGUAGES.get(current_lang, {}).get('native', 'English'),
        'languages': LANGUAGES,
        'is_hindi': current_lang == 'hi',
        'is_english': current_lang == 'en',
    }