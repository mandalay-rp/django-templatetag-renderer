from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def greeting(name):
    return format_html("<p>Привет, <b>{}</b>!</p>", name)


@register.simple_tag
def counter(start, step, count):
    items = "".join(f"<li>{start + i * step}</li>" for i in range(count))
    return format_html('<ul class="counter">{}</ul>', mark_safe(items))


@register.simple_tag
def price(amount, currency="RUB", locale="ru"):
    formatted = f"{amount:,}".replace(",", " ")
    return format_html(
        '<span class="price price--{}">{} {}</span>',
        locale, formatted, currency,
    )


@register.simple_tag
def show_value(value):
    """Возвращает repr переданного значения — полезно для проверки типов."""
    return format_html("<code>{}</code>", repr(value))


@register.simple_tag(takes_context=True)
def whoami(context):
    req = context.get("request")
    return format_html("<code>{}</code>", req.path if req else "no-request")
