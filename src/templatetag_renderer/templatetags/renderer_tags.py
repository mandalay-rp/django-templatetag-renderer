from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

from django import template
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import SafeString, mark_safe

register = template.Library()


@register.simple_tag
def render_slot(
    tag_name: str,
    *args: Any,
    lib: str | None = None,
    element: str = "div",
    **kwargs: Any,
) -> SafeString:
    """Строит HTML-элемент с data-атрибутом, ведущим на /render/.

    Позиционные аргументы идут сразу после имени тега, именованные —
    как key=value. Зарезервированы только ``lib`` и ``element``;
    всё остальное уходит в query-string для /render/.

    Пример:
        {% render_slot "greeting" "World" %}
        {% render_slot "counter" 0 2 5 %}
        {% render_slot "price" 999 currency="USD" %}
        {% render_slot "greeting" "Alice" lib="shop_tags" %}
        {% render_slot "greeting" "World" element="aside" %}
    """
    query_items: list[tuple[str, str]] = [("args", str(a)) for a in args]
    for key, value in kwargs.items():
        query_items.append((key, str(value)))

    if lib:
        url = reverse("templatetag_renderer:render-tag-lib", args=[lib, tag_name])
    else:
        url = reverse("templatetag_renderer:render-tag", args=[tag_name])

    if query_items:
        url = f"{url}?{urlencode(query_items)}"

    return format_html(
        '<{element} class="renderer-slot" data-tag-url="{}"></{element}>',
        mark_safe(url),
        element=element,
    )
