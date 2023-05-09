from dependency_injector.wiring import inject, Provide
from django.http import HttpResponse, HttpRequest
from django.template import loader

from core.services import IProductService


@inject
def index(request: HttpRequest,
          product_service: IProductService = Provide["product_service"], ):
    products_list = product_service.get_all_products()
    template = loader.get_template("products/index.html")
    context = {
        "products_list": products_list,
    }
    return HttpResponse(template.render(context, request))
