from django import template

register = template.Library()

@register.filter
def split(string, sep=' '):
    return string.split(sep)[0]
