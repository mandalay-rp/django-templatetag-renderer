# django-templatetag-renderer

<!-- ![ci image](https://github.com/mandalay-rp/django-templatetag-renderer/actions/workflows/ci.yml/badge.svg) -->
<!-- ![](https://img.shields.io/pypi/v/django-templatetag-renderer.svg) -->
<!-- ![](https://img.shields.io/pypi/pyversions/django-templatetag-renderer.svg) -->
![](https://img.shields.io/badge/django-3.2%20%7C%204.2%20%7C%205.0%20%7C%205.1-blue)
![](https://img.shields.io/badge/License-MIT-yellow.svg)

Динамический рендерер для получения html-кода, возвращаемого шаблонными тегами Django (templatetags). 
Позволяет отрендерить любой simple_tag из любого приложения проекта по HTTP-запросу — без импорта этих тегов и без знания об их существовании на этапе разработки.
Плюс JS-загрузчик, который подставляет результат в HTML-элементы с data-tag-url.

## Установка:
```bash

pip install django-templatetag-renderer
# или
uv add django-templatetag-renderer
```
## Быстрый старт
### Добавьте приложение в INSTALLED_APPS:
    
```python
INSTALLED_APPS = [
    # ...
    "django.contrib.staticfiles",
    "templatetag_renderer",
]
```
### Подключите URL-ы:
```python
# urls.py
from django.urls import include, path

urlpatterns = [
    path("render/", include("templatetag_renderer.urls")),
]
```
### Используйте в шаблоне:
```django
    {% load static renderer_tags %}
    <link rel="stylesheet" href="{% static 'templatetag_renderer/renderer.css' %}">

    {% render_slot "greeting" "World" %}
    {% render_slot "counter" 0 2 5 %}
    {% render_slot "price" 999 currency="USD" %}
    {% render_slot "greeting" "Alice" lib="shop_tags" element="aside" %}

    <script src="{% static 'templatetag_renderer/renderer.js' %}"></script>
```
## HTTP API
### URLS
```
/render/<template_tag_name>/  Найти <template_tag_name> в любой библиотеке проекта и отрендерить
/render/<tag_lib>/<template_tag_name>/    Явно указать библиотеку <tag_lib> и тег <template_tag_name>
```
Аргументы — в query-string:
```
?args=VALUE — позиционный (можно повторять).
?<name>=VALUE — именованный (keyword).
```
Автоматическое приведение типов: int, float, true/false, none, иначе строка.

```bash

curl 'http://localhost:8000/render/greeting/?args=World'
curl 'http://localhost:8000/render/counter/?args=0&args=2&args=5'
curl 'http://localhost:8000/render/price/?args=1234567&currency=USD'
curl 'http://localhost:8000/render/shop_tags/greeting/?args=Alice'
```
## Как это работает
```text
1. django.template.backends.django.get_installed_libraries() обходит всеINSTALLED_APPS, находит подпакеты templatetags/ и возвращает словарь {short_name: dotted_path}.
2. View импортирует найденный модуль и проверяет наличие тега в register.tags.
3. Собирает шаблон на лету: {% load shop_tags %}{% counter _p0 _p1 _p2 %}
Значения из URL кладутся в контекст под служебными именами _p0,
_k_currency — тег получает уже типизированные значения.

Template(src).render(RequestContext(request, ctx)) → HttpResponse.
```
## JS API
```javascript

// точечный рендер
TemplatetagRenderer.renderSlots(document.querySelector("#sidebar"));

// хуки
TemplatetagRenderer.setOptions({
  fetcher: customFetch,           // свой fetch (CSRF, ретраи, кэш)
  onRender(el, html) { /* ... */ },
  onError(el, err)   { /* ... */ },
});
```
## Разработка

### Проект использует uv.
```bash

git clone https://github.com/mandalay-rp/django-templatetag-renderer
cd django-templatetag-renderer
uv sync                     # создаст .venv и uv.lock
uv run pytest -v            # тесты
uv run ruff check .         # линтер
uv run ruff format .        # формат

# запустить минимальный пример
cd examples/minimal
uv run python manage.py runserver
```
### Сборка дистрибутивов
```bash

uv build                    # wheel + sdist в ./dist/
uv publish                  # публикация на PyPI (нужен токен или trusted publishing)
```
## Безопасность

По умолчанию рендерятся все теги проекта. На проде:
* закройте /render/ аутентификацией или ограничением по IP;
* задайте белый список разрешённых тегов;
* помните, что JS вставляет HTML без санитайза (как |safe);
* не выставляйте эндпоинт в публичный интернет без необходимости.

## Лицензия

MIT.
