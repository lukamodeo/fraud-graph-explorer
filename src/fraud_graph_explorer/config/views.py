# src/fraud_graph_explorer/config/views.py

# Fraud Graph Explorer
# Copyright (C) 2026 Luca Amodeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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