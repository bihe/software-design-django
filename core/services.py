from abc import ABC, abstractmethod
from typing import List

from django.db import models

from core.models import Product

"""
In this code, we are defining the interfaces for the services.
Interfaces are abstract classes that declare a set of methods that must be implemented
by any concrete class that implements the interface.
"""


# here we define the interfaces for the services
class IProductService(ABC):
    # Declare abstract methods for ProductService
    @abstractmethod
    def get_all_products(self) -> List[Product]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> models.QuerySet:
        pass

    @abstractmethod
    def get_price(self, product: Product) -> float:
        pass


class ICustomerService(ABC):
    @abstractmethod
    def has_credit(self, customer) -> bool:
        pass

    @abstractmethod
    def redeem_credit(self, customer, amount) -> bool:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> models.QuerySet:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> models.QuerySet:
        pass
