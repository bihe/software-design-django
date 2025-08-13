from django import template

from core.models import Product

register = template.Library()


@register.inclusion_tag("orders/add_to_basket_form.html")
def button_add_to_basket(product: Product):
    # Determine the additional functionality based on the context
    # ...
    # Generate the HTML code or functionality dynamically
    return {"product": product}


@register.inclusion_tag("orders/basket_link.html", takes_context=True)
def show_basket_Link(context):
    request = context["request"]
    product_list = request.session.get("product_list", [])
    basket_count = len(product_list)
    return {"basket_count": basket_count}
