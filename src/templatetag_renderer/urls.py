from django.urls import path

from . import views

app_name = "templatetag_renderer"

urlpatterns = [
    path("<str:lib_name>/<str:tag_name>/", views.render_tag, name="render-tag-lib"),
    path("<str:tag_name>/", views.render_tag, name="render-tag"),
]
