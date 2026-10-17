# Changelog

Все значимые изменения проекта документируются в этом файле.
Формат — [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/),
версионирование — [SemVer](https://semver.org/lang/ru/).

## [Unreleased]

## [0.1.0] — 2026-10-17

### Added
- Первый релиз.
- Динамический рендерер для получения html-кода, возвращаемого шаблонными тегами Django (templatetags). 
- Автоматическое приведение типов query-параметров (`int`/`float`/`bool`/`None`).
- Поддержка `takes_context=True` (теги получают настоящий `RequestContext`).
- Шаблонный тег `{% render_slot %}` для генерации HTML-слотов с `data-tag-url`.
- Клиентский загрузчик `renderer.js` с `MutationObserver` и хуками
  `onRender` / `onError` / `fetcher`.
- Публичный URL namespace `templatetag_renderer`.
- Полный набор unit-тестов (Django `SimpleTestCase` + pytest).
