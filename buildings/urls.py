from django.urls import path

from . import views


app_name = "buildings"
urlpatterns = [
    path("", views.index, name="index"),
    path("buildings/<int:pk>", views.building_detail, name="building-detail"),
]
