from dependency_injector import containers, providers

from orders.services import OrderService
from products.models import Product
#from product_alternative.services import ProductServiceAlternative
from products.services import ProductService


# define a container class and declare its dependencies
class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    product_service = providers.Singleton(
        ProductService,
    )

    product_factory = providers.Factory(Product, id=int, name=str, description=str )

    order_service = providers.Singleton(
        OrderService, product_service=product_service
    )
