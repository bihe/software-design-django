from django.urls import path

from . import views

app_name = "customers"

urlpatterns = [
    path("profile/<int:pk>/", views.CustomerProfileView.as_view(), name="customer-detail"),
    path("customer/<int:pk>/", views.CustomerUpdateView.as_view(), name="customer-update"),
]
