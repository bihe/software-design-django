from abc import ABC, abstractmethod
from typing import List

from core.models import Product


# here we define the interfaces for the services
class IProductService(ABC):
    @abstractmethod
    def get_all_products(self) -> List[Product]:
        pass

    @abstractmethod
    def get_price(self, product: Product) -> float:
        pass


class IOrderService(ABC):
    # the order service needs the product service, so we pass it as a parameter
    @abstractmethod
    def __init__(self, product_service: IProductService) -> None:
        pass

    @abstractmethod
    def get_all_products(self) -> List[Product]:
        pass


class ICustomerService(ABC):
    @abstractmethod
    def has_credit(self, Customer) -> bool:
        pass
