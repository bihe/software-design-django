from dependency_injector.wiring import inject, Provide
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from core.models import Product
from core.services import IOrderService


@inject
def index(request: HttpRequest,
          # Provide is a special object used in dependency injection frameworks to specify that the required object
          # should be provided by the framework itself, rather than being instantiated by the code.
          order_service: IOrderService = Provide["order_service"],
          ) -> HttpResponse:
    return HttpResponse("Hello, world. You're at the orders index." + order_service.get_all_products()[0].name
                        + " ")


@csrf_exempt
@inject
def add_to_basket(request: HttpRequest, order_service: IOrderService = Provide["order_service"], ) -> HttpResponse:
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id is None:
            return HttpResponseBadRequest("Missing 'product_id' parameter")

        # this does not work, because Product in abstract
        # product = get_object_or_404(Product, pk=product_id)

        # check if product exists
        product: Product = order_service.get_product(product_id)
        if product is None:
            raise Http404("Product does not exist")

        # Retrieve the list of products from the session
        product_list = request.session.get('product_list', [])

        # Add the product ID to the list
        product_list.append(product_id)

        # Update the session with the modified product list
        request.session['product_list'] = product_list
        """
        The request.META.get('HTTP_REFERER') value represents the URL of the previous page the user visited. 
        By passing it as the argument to redirect(), you can redirect the user back to that page. 
        Note that request.META.get('HTTP_REFERER') might be None if the browser or client doesn't 
        provide the referrer information.
        """
        return redirect(request.META.get('HTTP_REFERER'))

    return HttpResponseBadRequest("Invalid request method")
