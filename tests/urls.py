from django.urls import include, path

urlpatterns = [
    path("render/", include("templatetag_renderer.urls")),
]
