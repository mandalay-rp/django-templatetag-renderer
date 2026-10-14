from django.template.backends.django import get_installed_libraries
from django.test import SimpleTestCase

from templatetag_renderer.views import _coerce, _find_library_with_tag


class DiscoveryTests(SimpleTestCase):
    def test_shop_tags_library_is_visible(self):
        libs = get_installed_libraries()
        assert "shop_tags" in libs

    def test_find_library_by_tag_name(self):
        assert _find_library_with_tag("greeting") == "shop_tags"
        assert _find_library_with_tag("counter") == "shop_tags"

    def test_find_library_respects_hint(self):
        assert _find_library_with_tag("greeting", lib_name="shop_tags") == "shop_tags"

    def test_find_library_respects_wrong_hint(self):
        assert _find_library_with_tag("greeting", lib_name="not_shop_tags") is None

    def test_find_library_returns_none_for_unknown_tag(self):
        assert _find_library_with_tag("no_such_tag_anywhere") is None


class CoerceTests(SimpleTestCase):
    def test_int(self):
        assert _coerce("42") == 42 and isinstance(_coerce("42"), int)

    def test_float(self):
        assert _coerce("3.14") == 3.14 and isinstance(_coerce("3.14"), float)

    def test_bool(self):
        assert _coerce("true") is True
        assert _coerce("false") is False
        assert _coerce("TRUE") is True

    def test_none(self):
        assert _coerce("none") is None
        assert _coerce("None") is None

    def test_string_fallback(self):
        assert _coerce("hello") == "hello"
