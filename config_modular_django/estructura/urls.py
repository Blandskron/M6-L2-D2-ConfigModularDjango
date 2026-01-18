from django.urls import path

from . import views

app_name = "estructura"

urlpatterns = [
    path("hola/", views.hola, name="hola"),
    path("", views.home, name="home"),
    path("mvt/", views.mvt, name="mvt"),
]
