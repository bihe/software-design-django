from dependency_injector.wiring import Provide, inject
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from core.models import Product
from core.services import IOrderService
from orders.services import OrderModel

SESSION_ORDER = "sess.order"
SESSION_PRODUCTLIST = "product_list"


def set_order_session(request: HttpRequest, order: OrderModel):
    request.session[SESSION_ORDER] = OrderModel().dump(order)


def get_order_session(request: HttpRequest) -> OrderModel:
    return request.session.get(SESSION_ORDER)


def del_order_session(request: HttpRequest):
    request.session.delete(SESSION_ORDER)


def set_productlist_session(request: HttpRequest, order: OrderModel):
    request.session[SESSION_PRODUCTLIST] = OrderModel().dump(order)


def get_productlist_session(request: HttpRequest) -> OrderModel:
    return request.session.get(SESSION_ORDER)


def del_productlist_session(request: HttpRequest):
    request.session.delete(SESSION_PRODUCTLIST)


@inject
def basket_overview(request: HttpRequest, order_service: IOrderService = Provide["order_service"]) -> HttpResponse:
    product_list = request.session.get("product_list", [])

    order_model: OrderModel = order_service.get_order_model(request.user, product_list)

    set_order_session(request, OrderModel().dump(order_model))
    context = {
        "order": order_model,
    }
    return render(request, "orders/basket_overview.html", context)


@csrf_exempt
@inject
def add_to_basket(
    request: HttpRequest,
    order_service: IOrderService = Provide["order_service"],
) -> HttpResponse:
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        if product_id is None:
            return HttpResponseBadRequest("Missing 'product_id' parameter")

        # this does not work, because Product in abstract
        # product = get_object_or_404(Product, pk=product_id)

        # check if product exists
        product: Product = order_service.get_product(product_id)
        if product is None:
            raise Http404("Product does not exist")

        # Retrieve the list of products from the session
        product_list: list[Product] = request.session.get("product_list", [])

        # Add the product ID to the list
        product_list.append(product_id)

        # Update the session with the modified product list
        request.session["product_list"] = product_list

        """
        The request.META.get('HTTP_REFERER') value represents the URL of the previous page the user visited.
        By passing it as the argument to redirect(), you can redirect the user back to that page.
        Note that request.META.get('HTTP_REFERER') might be None if the browser or client doesn't
        provide the referrer information.
        """
        return redirect(request.META.get("HTTP_REFERER"))

    return HttpResponseBadRequest("Invalid request method")


@inject
def place_order(request: HttpRequest, order_service: IOrderService = Provide["order_service"]) -> HttpResponse:
    order_id = order_service.create_order(get_order_session(request))
    if order_id is None:
        return HttpResponseBadRequest("Could not create order")
    else:
        del_productlist_session(request)
        del_order_session(request)
        return HttpResponse("Order created with id: " + str(order_id))


def clear_basket(request: HttpRequest) -> HttpResponse:
    """
    the basket is cleared by removing entries from the session
    """
    del_productlist_session(request)
    del_order_session(request)
    return redirect("orders:basket_overview")
