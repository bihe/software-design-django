from django.db import models

from orders.managers import OrderManager
from orders.settings import CUSTOMER_MODEL, PRODUCT_MODEL


# Create your models here.
class Order(models.Model):
    objects: OrderManager = OrderManager()  # use our own manager
    # object / database fields
    user: models.ForeignKey = models.ForeignKey(to=CUSTOMER_MODEL, on_delete=models.PROTECT, )


class OrderPosition(models.Model):
    # Django does not support composite primary keys, so we have to use a unique_together constraint
    # ticket is open for this since 18 years!!!
    class Meta:
        unique_together = (('order', 'pos'),)

    order: models.ForeignKey[Order] = models.ForeignKey(Order, on_delete=models.CASCADE)
    pos: models.PositiveIntegerField = models.PositiveIntegerField()
    product: models.ForeignKey = models.ForeignKey(PRODUCT_MODEL, on_delete=models.PROTECT)
    quantity: models.IntegerField = models.IntegerField()
    price: models.FloatField = models.FloatField()
