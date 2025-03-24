from django import template

register = template.Library()

@register.filter
def capitalize_first(value):
    if not value:
        return ""
    return value[0].upper() + value[1:].lower()

@register.filter
def reduce(value, limit):
    if value:
        return value[:limit]
    return ""
