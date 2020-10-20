from django import template

register = template.Library()

@register.filter # register the template filter with django
def get_string_as_list(value): # Only one argument.
    """Evaluate a string if it contains []"""
    if '[' and ']' in value:
        return eval(value)