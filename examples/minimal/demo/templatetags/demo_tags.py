from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def hello(name):
    return format_html("<p>Hello, <b>{}</b>!</p>", name)
