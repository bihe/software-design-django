from dependency_injector.wiring import Provide, inject
from django.http import HttpRequest
from django.shortcuts import render

from .services import ProductService


@inject
def index(
    request: HttpRequest,
    # Provide is a special object used in dependency injection frameworks to specify that the required object
    # should be provided by the framework itself, rather than being instantiated by the code.
    product_service: ProductService = Provide["product_service"],
):
    # get all products from the product service
    # (note that we are not using a concrete product service, but an interface
    products_list = product_service.get_all_products()
    # the context is a dictionary that is used to pass data to the template
    context = {
        "products_list": products_list,
    }
    return render(request, "products/index.html", context)
