from django.urls import path

from . import views

app_name = "orders"

# Map URLs to views
urlpatterns = [
    # Map the index URL of the "orders" application to the index view
    path("", views.order_overview, name="order_overview"),
    path("basket", views.basket_overview, name="basket_overview"),
    path("add_to_basket", views.add_to_basket, name="add_to_basket"),
    path("place_oder", views.place_order, name="place_order"),
    path("clear_basket", views.clear_basket, name="clear_basket"),
    path("<order_id>", views.order_detail, name="order_detail"),
]
