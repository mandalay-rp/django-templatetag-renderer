from django.test import SimpleTestCase


class RenderTagViewTests(SimpleTestCase):
    def test_renders_simple_tag_with_positional_arg(self):
        r = self.client.get("/render/greeting/", {"args": ["World"]})
        assert r.status_code == 200
        assert r["Content-Type"] == "text/html; charset=utf-8"
        body = r.content.decode()
        assert "Привет" in body
        assert "<b>World</b>" in body

    def test_renders_tag_with_multiple_positional_args(self):
        r = self.client.get("/render/counter/", {"args": ["0", "2", "5"]})
        assert r.status_code == 200
        body = r.content.decode()
        for n in (0, 2, 4, 6, 8):
            assert f"<li>{n}</li>" in body

    def test_keyword_arguments_are_passed(self):
        r = self.client.get("/render/price/", {"args": ["999"], "currency": "USD"})
        assert r.status_code == 200
        assert "USD" in r.content.decode()

    def test_explicit_library_in_url(self):
        r = self.client.get("/render/shop_tags/greeting/", {"args": ["Alice"]})
        assert r.status_code == 200
        assert "<b>Alice</b>" in r.content.decode()

    def test_takes_context_receives_real_request(self):
        r = self.client.get("/render/whoami/")
        assert r.status_code == 200
        assert "/render/whoami/" in r.content.decode()

    def test_unknown_tag_returns_404(self):
        assert self.client.get("/render/no_such_tag/").status_code == 404

    def test_unknown_library_returns_404(self):
        assert self.client.get("/render/nope_lib/greeting/").status_code == 404

    def test_post_is_not_allowed(self):
        r = self.client.post("/render/greeting/", {"args": ["x"]})
        assert r.status_code == 405


class TypeCoercionTests(SimpleTestCase):
    def test_int_coercion(self):
        r = self.client.get("/render/counter/", {"args": ["10", "1", "3"]})
        body = r.content.decode()
        assert "<li>10</li>" in body
        assert "<li>11</li>" in body
        assert "<li>12</li>" in body

    def test_float_coercion(self):
        r = self.client.get("/render/show_value/", {"args": ["3.14"]})
        assert r.status_code == 200
        assert "3.14" in r.content.decode()

    def test_bool_and_none_coercion(self):
        for raw, expected in (("true", "True"), ("false", "False"), ("none", "None")):
            r = self.client.get("/render/show_value/", {"args": [raw]})
            assert expected in r.content.decode()

    def test_string_stays_string(self):
        r = self.client.get("/render/show_value/", {"args": ["hello"]})
        assert "'hello'" in r.content.decode()
