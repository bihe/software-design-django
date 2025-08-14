from django.db import models

# Create your models here.
from core.models import Product
from products.managers import ProductManager


# this is the concrete model that we will use for the project
class Product(Product):
    objects: ProductManager = ProductManager()

    class Meta:
        db_table: str = "products"

    # we are adding a price field to the product model
    price: float = models.FloatField()
