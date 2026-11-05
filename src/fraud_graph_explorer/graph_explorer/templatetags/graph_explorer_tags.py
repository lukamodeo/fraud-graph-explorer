# src/fraud_graph_explorer/graph_explorer/templatetags/graph_explorer_tags.py

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

from django import template
from fraud_graph_explorer.domain_schema import get_country_flag

# This register object is how we tell Django this is a custom template tag library
register = template.Library()


@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Given a dictionary and a key, return the value.
    Allows doing dict[key] inside Django templates.
    """
    if hasattr(dictionary, 'get'):
        return dictionary.get(key)
    return None


@register.filter(name='get_attr')
def get_attr(obj, attr):
    return getattr(obj, attr, "")


# Split filter for lists
@register.filter(name='split')
def split(value, separator="|"):
    return value.split(separator) if value else []



# Custom template filter for converting ISO country codes to flag emojis.
"""Usage in templates:
    {% load country_flags %}
    ...
    {{ country_code|country_flag }}
"""
@register.filter
def country_flag(country_code):
    """
    Convert a 2-letter ISO country code (e.g., 'IT', 'GB') into a
    Unicode regional indicator flag emoji (e.g., '🇮🇹', '🇬🇧').

    Returns an empty string if country_code is None, empty, or not
    a 2-letter string.
    """
    if not country_code or not isinstance(country_code, str):
        return ''
    if len(country_code) != 2:
        return ''
    return get_country_flag(country_code.upper())