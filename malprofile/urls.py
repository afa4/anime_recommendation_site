from django.urls import path

from . import views

urlpatterns = [
    path("", views.profile, name="profile"),
    path("submit", views.anime_submit, name="anime_submit"),
]
