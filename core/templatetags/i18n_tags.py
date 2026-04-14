from django import template
from django.utils.safestring import mark_safe
from core.translation import translate_text

register = template.Library()

@register.simple_tag(takes_context=True)
def t(context, text):
    """Translate a string using current language from context."""
    lang = context.get('current_lang', 'en')
    if lang == 'en' or not text:
        return text
    return translate_text(str(text), lang)

@register.filter(name='translate')
def translate_filter(text, lang):
    """Template filter: {{ "some text"|translate:current_lang }}"""
    if lang == 'en' or not text:
        return text
    return translate_text(str(text), lang)