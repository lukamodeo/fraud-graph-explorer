# src/fraud_graph_explorer/config/views.py

"""Project-level views (auth, etc.)."""

from django.contrib.auth.views import LoginView
from django.utils.translation import get_language

from .login_translations import LOGIN_STRINGS


class CustomLoginView(LoginView):
    """LoginView with browser-language-aware translations."""
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = get_language().lower()[:2]
        if lang == 'en':
            lang = 'en-gb'
        context['login_ui'] = LOGIN_STRINGS.get(lang, LOGIN_STRINGS['en-gb'])
        return context