from typing import List

from dependency_injector.wiring import inject, Provide

from core.models import Product
from core.services import IOrderService


class OrderService(IOrderService):

    @inject
    def __init__(self, product_service: Provide("product_service")):
        self.product_service = product_service

    def get_all_products(self) -> List[Product]:
        return self.product_service.get_all_products()
        pass
