from django.db import models

# Create your models here.
from core.models import Product
from products.managers import ProductManager


class ProductBase(Product):

    class Meta:
        swappable: str = "PRODUCT_MODEL"
        db_table: str = "products_base"


class Product(ProductBase):
    objects: ProductManager = ProductManager()

    class Meta:
        db_table: str = "products_simple"

    price: float = models.FloatField()
