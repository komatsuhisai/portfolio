from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    """引数 arg を value から引く"""
    return value - arg

    