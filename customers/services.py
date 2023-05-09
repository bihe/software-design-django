from core.models import Customer
from core.services import ICustomerService


class CustomerService(ICustomerService):

    def has_credit(self, customer: Customer) -> bool:
        return customer.credit > 0
