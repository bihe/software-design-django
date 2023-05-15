from django.db import models


from core.services import ICustomerService
from customers.models import Customer


class CustomerService(ICustomerService):
    """
        Implementation of the ICustomerService interface for checking if a customer has any credit or not.
    """
    def has_credit(self, customer: Customer) -> bool:
        return customer.credit > 0

    def get_by_id(self, id: int) -> models.QuerySet:
        try:
            return Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return None

    def get_by_username(self, username: str) -> models.QuerySet:
        try:
            return Customer.objects.get(username=username)
        except Customer.DoesNotExist:
            return None
