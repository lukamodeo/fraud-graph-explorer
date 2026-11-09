# src/fraud_graph_explorer/config/context_processors.py

from .common_translations import COMMON_STRINGS


def common_translations(request):
    """Inject common UI strings (login, lockout, screen warning) into
    every template context. Runs on ALL pages via context processor."""
    lang = getattr(request, 'LANGUAGE_CODE', 'en')[:2].lower()
    if lang == 'en':
        lang = 'en-gb'
    return { 'common_ui': COMMON_STRINGS.get(lang, COMMON_STRINGS['en-gb']) }