# Minimal example

```bash
# из корня репозитория
uv sync
cd examples/minimal
uv run python manage.py runserver

Затем откройте:
http://127.0.0.1:8000/render/hello/?args=World
