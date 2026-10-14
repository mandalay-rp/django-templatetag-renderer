from urllib.parse import urlencode

from django import template
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def render_slot(tag_name, lib_name=None, tag="div", *args, **kwargs):
    """
    Строит HTML-элемент с data-атрибутом, ведущим на /render/.

    Пример:
        {% render_slot "greeting" args="World" %}
        {% render_slot "counter" args=0 args=2 args=5 %}
        {% render_slot "price" args=999 currency="USD" %}
        {% render_slot "greeting" lib_name="shop_tags" args="Alice" tag="aside" %}
    """
    positional = []
    if "args" in kwargs and isinstance(kwargs["args"], (list, tuple)):
        positional = list(kwargs.pop("args"))
    elif "args" in kwargs:
        positional = [kwargs.pop("args")]

    query_items: list[tuple[str, str]] = [("args", str(v)) for v in positional]
    for key, value in kwargs.items():
        query_items.append((key, str(value)))

    if lib_name:
        url = reverse("templatetag_renderer:render-tag-lib", args=[lib_name, tag_name])
    else:
        url = reverse("templatetag_renderer:render-tag", args=[tag_name])

    if query_items:
        url = f"{url}?{urlencode(query_items)}"

    return format_html(
        '<{tag} class="renderer-slot" data-tag-url="{}"></{tag}>',
        mark_safe(url),
        tag=tag,
    )
