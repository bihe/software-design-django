import datetime
from typing import List, Optional

from django.db import models


# "A Manager is the interface through which database query operations are
#  provided to Django models. At least one Manager exists for every model
#  in a Django application."
#  (https://docs.djangoproject.com/en/5.2/topics/db/managers/)
class ProductManager(models.Manager):
    def get_by_id(self, id: int) -> Optional["Product"]:
        # Query for Product object by id
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def get_by_name(self, name: str) -> List["Product"]:
        # Query for Product objects by name
        return self.get_queryset().filter(name=name)

    def get_by_price_range(self, min_price: float, max_price: float) -> List["Product"]:
        # Query for Product objects by price range
        return self.get_queryset().filter(price__gte=min_price, price__lte=max_price)


# this is the concrete model that we will use for the project
# https://docs.djangoproject.com/en/5.2/topics/db/models/
class Product(models.Model):
    objects: ProductManager = ProductManager()

    class Meta:
        db_table: str = "products"

    # each product has a name and a description
    name: str = models.CharField(max_length=200)
    description: str = models.TextField()
    price: float = models.FloatField()
    created_at: datetime.datetime = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self) -> str:
        return self.name
