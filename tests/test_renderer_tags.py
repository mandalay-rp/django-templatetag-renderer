from django.template import Context, Template
from django.test import SimpleTestCase


def render(src: str) -> str:
    return Template("{% load renderer_tags %}" + src).render(Context({}))


class RenderSlotTagTests(SimpleTestCase):
    def test_basic_slot(self):
        html = render('{% render_slot "greeting" "World" %}')
        assert "data-tag-url=" in html
        assert 'class="renderer-slot"' in html
        assert "/render/greeting/" in html
        assert "args=World" in html

    def test_multiple_positional(self):
        html = render('{% render_slot "counter" 0 2 5 %}')
        assert "args=0" in html
        assert "args=2" in html
        assert "args=5" in html

    def test_lib_in_url(self):
        html = render('{% render_slot "greeting" "Alice" lib="shop_tags" %}')
        assert "/render/shop_tags/greeting/" in html

    def test_custom_element(self):
        html = render('{% render_slot "greeting" "X" element="section" %}')
        assert "<section" in html and "</section>" in html

    def test_keyword_arguments(self):
        html = render('{% render_slot "price" 999 currency="USD" %}')
        assert "args=999" in html
        assert "currency=USD" in html

    def test_mixed_positional_and_keyword(self):
        html = render('{% render_slot "price" 500 currency="EUR" locale="de" %}')
        assert "args=500" in html
        assert "currency=EUR" in html
        assert "locale=de" in html
