from django import template

register = template.Library()

@register.filter
def custom_div(dividend, divisor):
    if divisor == 0:
        return ''
    return dividend / divisor