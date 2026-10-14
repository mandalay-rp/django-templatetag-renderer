from django.template import Context, Template
from django.test import SimpleTestCase


def render(src):
    return Template("{% load renderer_tags %}" + src).render(Context({}))


class RenderSlotTagTests(SimpleTestCase):
    def test_basic_slot(self):
        html = render('{% render_slot "greeting" args="World" %}')
        assert "data-tag-url=" in html
        assert 'class="renderer-slot"' in html
        assert "/render/greeting/" in html
        assert "args=World" in html

    def test_multiple_positional(self):
        html = render('{% render_slot "counter" args=0 args=2 args=5 %}')
        assert "args=2" in html and "args=5" in html

    def test_lib_name_in_url(self):
        html = render('{% render_slot "greeting" lib_name="shop_tags" args="Alice" %}')
        assert "/render/shop_tags/greeting/" in html

    def test_custom_tag_name(self):
        html = render('{% render_slot "greeting" args="X" tag="section" %}')
        assert "<section" in html and "</section>" in html

    def test_keyword_arguments(self):
        html = render('{% render_slot "price" args=999 currency="USD" %}')
        assert "currency=USD" in html
