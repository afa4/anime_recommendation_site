from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("submit", views.anime_submit, name="anime_submit"),
]
