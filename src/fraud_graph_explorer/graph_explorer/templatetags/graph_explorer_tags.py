# src/fraud_graph_explorer/graph_explorer/templatetags/graph_explorer_tags.py

from django import template

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