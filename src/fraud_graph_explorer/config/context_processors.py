# config/context_processors.py

from .login_translations import LOCKOUT_STRINGS


def lockout_translations(request):
    """Inject lockout page translations based on browser language.

    Uses request.LANGUAGE_CODE set by LocaleMiddleware.
    Works in templates rendered by django-axes (which has no custom view
    to inject context the way CustomLoginView does for the login page).
    """
    # request.LANGUAGE_CODE is like 'it', 'en-us', 'fr-fr' — take first 2 chars
    lang = getattr(request, 'LANGUAGE_CODE', 'en')[:2].lower()
    return { 'lockout_ui': LOCKOUT_STRINGS.get(lang, LOCKOUT_STRINGS['en']) }