import importlib

from django.http import Http404, HttpResponse
from django.template import RequestContext, Template, TemplateSyntaxError
from django.template.backends.django import get_installed_libraries
from django.utils.html import escape
from django.views.decorators.http import require_GET
from django.core.cache import cache


def _coerce(value: str):
    """Строку из query-string превращаем в int/float/bool/None, если похоже."""
    low = value.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low == "none":
        return None
    for cast in (int, float):
        try:
            return cast(value)
        except ValueError:
            continue
    return value


def _find_library_with_tag(tag_name: str, lib_name: str | None = None) -> str | None:
    """
    Ищет шаблонную библиотеку (то, что пишут в {% load %}) по имени тега.
    Обходит все INSTALLED_APPS через штатное API Django.
    """
    cache_key = 'tag_name_lib_name_map'

    cached_map = cache.get(cache_key) or {}

    if tag_name in cached_map:
        return cached_map[tag_name]

    libraries = get_installed_libraries()  # {short_name: 'app.templatetags.module'}
    for name, module_path in libraries.items():
        if lib_name and name != lib_name:
            continue
        try:
            module = importlib.import_module(module_path)
        except ImportError:
            continue
        register = getattr(module, "register", None)
        if register and tag_name in register.tags:
            cached_map[tag_name] = name
            cache.set(cache_key, cached_map)
            return name
    return None


@require_GET
def render_tag(request, tag_name: str, lib_name: str | None = None):
    """
    Универсальный view — рендерит любой templatetag из любого приложения проекта.

    Примеры:
      /render/greeting/?args=World
      /render/counter/?args=0&args=2&args=5
      /render/price/?args=999&currency=RUB
      /render/shop_tags/greeting/?args=Alice
    """
    found_lib = _find_library_with_tag(tag_name, lib_name)
    if not found_lib:
        raise Http404(f"Templatetag {tag_name!r} не найден ни в одном приложении")

    positional = request.GET.getlist("args")
    kwargs = {k: v for k, v in request.GET.items() if k not in {"args", "lib"}}

    context: dict = {}
    arg_tokens: list[str] = []

    for i, raw in enumerate(positional):
        var = f"t_arg{i}"
        context[var] = _coerce(raw)
        arg_tokens.append(var)

    for k, raw in kwargs.items():
        var = f"_k_{k}"
        context[var] = _coerce(raw)
        arg_tokens.append(f"{k}={var}")

    template_src = (
        "{% load " + found_lib + " %}"
        "{% " + tag_name + (" " + " ".join(arg_tokens) if arg_tokens else "") + " %}"
    )

    try:
        tpl = Template(template_src)
        output = tpl.render(RequestContext(request, context))
    except TemplateSyntaxError as exc:
        raise Http404(f"Синтаксис тега неверен: {exc}") from exc
    except Exception as exc:  # noqa: BLE001
        return HttpResponse(
            f'<div class="error">{escape(str(exc))}</div>',
            status=500,
            content_type="text/html; charset=utf-8",
        )

    return HttpResponse(output, content_type="text/html; charset=utf-8")
