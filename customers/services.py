from core.models import Customer
from core.services import ICustomerService


class CustomerService(ICustomerService):
    """
        Implementation of the ICustomerService interface for checking if a customer has any credit or not.
    """
    def has_credit(self, customer: Customer) -> bool:
        return customer.credit > 0
