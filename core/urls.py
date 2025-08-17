from django.urls import path

from . import views

app_name = "core"

# Map URLs to views
urlpatterns = [
    # Map the index URL of the "core" application to the index view
    path("", views.index_view, name="index"),
    path("logout", views.logout_view, name="logout"),
    path("health", views.health_check, name="health_check"),
]
