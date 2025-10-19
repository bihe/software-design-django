from django.db import models

from customers.models import Customer
from products.models import Product

"""
The OrderManager class is a custom manager for the Order model.
It provides a method to retrieve an order by its ID.
"""


class OrderManager(models.Manager):
    # This method retrieves an order by its ID
    def get_by_id(self, id: int) -> models.QuerySet:
        # First, we get the queryset for all orders with the given ID
        qs: models.QuerySet = self.get_queryset().filter(id=id)
        # If there is exactly one order with the given ID, return it
        if qs.count() == 1:
            return qs.first()
        return None


# This file defines the models for our application
# The Order model represents an order made by a customer
class Order(models.Model):
    # We use our own manager to manage instances of the Order model
    objects: OrderManager = OrderManager()
    # The user field is a foreign key to the customer who made the order
    user: models.ForeignKey = models.ForeignKey(
        to=Customer,
        on_delete=models.PROTECT,
    )
    total_price: models.FloatField = models.FloatField()


# The OrderPosition model represents a single product in an order
class OrderPosition(models.Model):
    # Django does not support composite primary keys, so we have to use a unique_together constraint
    # ticket is open for this since 18 years!!! https://code.djangoproject.com/ticket/373
    class Meta:
        # This constraint ensures that each (order, pos) pair is unique
        unique_together = (("order", "pos"),)

    # The order field is a foreign key to the order that this position belongs to
    # add a related name to the foreign key, so that we can easily access the order positions of an order
    order: models.ForeignKey[Order] = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_positions"
    )
    # The pos field is an integer that represents the position of this order position within the order
    pos: models.PositiveIntegerField = models.PositiveIntegerField()
    # The product field is a foreign key to the product being ordered
    # We reference the model from the settings file, so that we can easily change it without having to change the code.
    # This is useful if we want to use a different product model for testing.
    # We also use the on_delete=models.PROTECT option to ensure that we cannot delete a product that is referenced by
    # an order position.
    product: models.ForeignKey = models.ForeignKey(Product, on_delete=models.PROTECT)
    # The quantity field is the number of units of the product being ordered
    quantity: models.IntegerField = models.IntegerField()
    # The price field is the price of the product being ordered
    price: models.FloatField = models.FloatField()
