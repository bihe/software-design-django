from django.urls import path

from . import views

# Map URLs to views
urlpatterns = [
    # Map the index URL of the "orders" application to the index view
    path("", views.index, name="index"),
]