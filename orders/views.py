from dependency_injector.wiring import inject, Provide
from django.http import HttpRequest, HttpResponse

from core.services import IOrderService


@inject
def index(request: HttpRequest,
          # Provide is a special object used in dependency injection frameworks to specify that the required object
          # should be provided by the framework itself, rather than being instantiated by the code.
          order_service: IOrderService = Provide["order_service"],
          ) -> HttpResponse:
    return HttpResponse("Hello, world. You're at the orders index." + order_service.get_all_products()[0].name
                        + " ")
