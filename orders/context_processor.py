from .views import get_productlist_session

# a custom Context-Processor is used to populate the global template scope with additional
# values. this example fetches the current basket-count and provides this value for templates
# creating a custom process is quite easy
#   https://docs.djangoproject.com/en/5.2/ref/templates/api/#writing-your-own-context-processors
#
# it needs to be configured in the settings.py TEMPLATES > OPTIONS > context_processors


def order_basket_count(request):
    basket_count = 0
    product_list = get_productlist_session(request)
    basket_count = len(product_list)
    return {"basket_count": basket_count}
