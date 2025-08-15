from dependency_injector.wiring import Provide, inject
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from core.models import Product
from core.services import IProductService
from orders.services import OrderModel, OrderService

SESSION_PRODUCTLIST = "product_list"


def set_productlist_session(request: HttpRequest, product_list: list[int]):
    request.session[SESSION_PRODUCTLIST] = product_list


def get_productlist_session(request: HttpRequest) -> list[int]:
    return request.session.get(SESSION_PRODUCTLIST, [])


def del_productlist_session(request: HttpRequest):
    del request.session[SESSION_PRODUCTLIST]


def get_order_model(request: HttpRequest, order_service: OrderService) -> OrderModel:
    order: OrderModel = None
    product_list: list[int] = get_productlist_session(request)
    if len(product_list) > 0:
        order = order_service.get_order_model(request.user, product_list)
    return order


@inject
def basket_overview(request: HttpRequest, order_service: OrderService = Provide["order_service"]) -> HttpResponse:
    context = {
        "order": {},
    }
    context["order"] = get_order_model(request, order_service)
    return render(request, "orders/basket_overview.html", context)


@inject
def order_overview(request: HttpRequest, order_service: OrderService = Provide["order_service"]) -> HttpResponse:
    context = {
        "orders": [],
    }
    context["orders"] = order_service.get_orders(request.user.username)
    return render(request, "orders/orders.html", context)


@inject
def order_detail(
    request: HttpRequest, order_id: int, order_service: OrderService = Provide["order_service"]
) -> HttpResponse:
    context = {
        "orders": [],
    }
    order = order_service.get_order(order_id)
    context = {
        "order": order,
    }
    return render(request, "orders/order.html", context)


@csrf_exempt
@inject
def add_to_basket(
    request: HttpRequest,
    product_service: IProductService = Provide["product_service"],
) -> HttpResponse:
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        if product_id is None:
            return HttpResponseBadRequest("Missing 'product_id' parameter")

        # this does not work, because Product in abstract
        # product = get_object_or_404(Product, pk=product_id)

        # check if product exists
        product: Product = product_service.get_by_id(product_id)
        if product is None:
            raise Http404("Product does not exist")

        # Retrieve the list of products from the session
        product_list: list[int] = get_productlist_session(request)
        # Add the product ID to the list
        product_list.append(product_id)

        # Update the session with the modified product list
        set_productlist_session(request, product_list)

        """
        The request.META.get('HTTP_REFERER') value represents the URL of the previous page the user visited.
        By passing it as the argument to redirect(), you can redirect the user back to that page.
        Note that request.META.get('HTTP_REFERER') might be None if the browser or client doesn't
        provide the referrer information.
        """
        return redirect(request.META.get("HTTP_REFERER"))

    return HttpResponseBadRequest("Invalid request method")


@inject
def place_order(request: HttpRequest, order_service: OrderService = Provide["order_service"]) -> HttpResponse:
    order_model: OrderModel = get_order_model(request, order_service)
    if order_model is None:
        return HttpResponseBadRequest("No order-model available")

    order_id = order_service.create_order(order_model)
    if order_id is None:
        return HttpResponseBadRequest("Could not create order")

    order = order_service.get_order(order_id)
    context = {
        "order": order,
    }

    del_productlist_session(request)
    return render(request, "orders/order.html", context)


def clear_basket(request: HttpRequest) -> HttpResponse:
    """
    the basket is cleared by removing entries from the session
    """
    del_productlist_session(request)
    return redirect("orders:basket_overview")
