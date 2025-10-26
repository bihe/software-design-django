from dataclasses import dataclass

from django.db import models, transaction

from customers.models import Customer


@dataclass
class CustomerModel:
    id: int = 0
    username: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    credit: float = 0.0

    @classmethod
    def from_customer(cls, customer: Customer) -> "CustomerModel":
        """Convert a Customer object to a CustomerModel dataclass."""
        return cls(
            id=customer.pk,
            username=customer.username or "",
            first_name=customer.first_name or "",
            last_name=customer.last_name or "",
            email=customer.email or "",
            credit=customer.credit or 0.0,
        )

    def to_customer(self, customer: Customer) -> Customer:
        """Update a Customer object with data from this CustomerModel."""
        customer.pk = self.id
        customer.username = self.username
        customer.first_name = self.first_name
        customer.last_name = self.last_name
        customer.email = self.email
        customer.credit = self.credit
        return customer


class CustomerService:
    def has_credit(self, customer: CustomerModel) -> bool:
        return customer.credit > 0

    def redeem_credit(self, customer: CustomerModel, amount: float) -> bool:
        if transaction.get_connection().in_atomic_block:
            # We are already in an atomic transaction, perform the credit redemption
            return self._perform_credit_redemption(customer, amount)
        else:
            # No active atomic transaction, create one and perform the credit redemption
            # at the end of the transaction, the changes will be committed to the database atomically
            with transaction.atomic():
                return self._perform_credit_redemption(customer, amount)

    def _perform_credit_redemption(self, customer: CustomerModel, amount: float) -> bool:
        # Lock the customer record for update, so that no other transaction can modify it
        customer_entity = Customer.objects.select_for_update().get(pk=customer.id)

        if customer_entity.credit is not None and customer_entity.credit >= amount:
            customer_entity.credit -= amount
            customer_entity.save()
            # in many other ORMs we do not need to call save() explicitly, as the ORM will keep track of
            # the changes and commit them to the database when the transaction is committed
            # personal remark (bid): Django ORM is not the best ORM out there ...
            return True
        else:
            return False

    def get_by_id(self, id: int) -> CustomerModel:
        try:
            customer_entity = Customer.objects.get(id=id)
            return CustomerModel.from_customer(customer_entity)
        except Customer.DoesNotExist:
            return None

    def get_by_username(self, username: str) -> CustomerModel:
        try:
            customer_entity = Customer.objects.get(username=username)
            return CustomerModel.from_customer(customer_entity)
        except Customer.DoesNotExist:
            return None

    def model_to_entity(self, customer: CustomerModel) -> models.QuerySet:
        try:
            return Customer.objects.get(id=customer.id)
        except Customer.DoesNotExist:
            return None
