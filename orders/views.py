from dependency_injector.wiring import inject, Provide
from django.http import HttpRequest, HttpResponse

from core.services import IOrderService

@inject
def index(request: HttpRequest,
          order_service: IOrderService = Provide["order_service"],
          ):
    return HttpResponse("Hello, world. You're at the orders index." + order_service.get_all_products()[0].name
                        + " ")
