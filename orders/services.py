from typing import List

from dependency_injector.wiring import inject, Provide

"""
Please note, that we are only importing the interfaces from the core module and not the concrete classes.
So this module can be used with any concrete product module implementation.
"""
from core.models import Product
from core.services import IOrderService

class OrderService(IOrderService):
    """
     A class that implements IOrderService interface to handle order related business logic.
     """

    # inject decorator is used to inject dependencies into the constructor method.
    @inject
    def __init__(self, product_service: Provide("product_service")):
        """
        Constructor method to initialize OrderService class.
        Args:
            product_service (Provide["product_service"]): An injected dependency to access the ProductService class.
                Provide("product_service") is a special constant value provided by the dependency_injector library that
                can be used as a placeholder when injecting dependencies.
                It indicates that the value for the argument should be provided by the dependency injection
                framework at runtime, rather than being explicitly passed in at the time of object creation.
        """
        self.product_service = product_service

    def get_all_products(self) -> List[Product]:
        return self.product_service.get_all_products()

    def get_product(self, product_id: int) -> Product:
        return self.product_service.get_by_id(product_id)

