from django.contrib.auth.models import AbstractUser
from django.db import models

from core.managers import CoreProductManager


# Create your models here.
# we define an abstract class Product here, so that we can use different types of products later
class Product(models.Model):

    objects = CoreProductManager()

    class Meta:
        abstract = True

    name: str = models.CharField(max_length=200)
    description: str = models.TextField()

    def __str__(self) -> str:
        return self.name


class Customer(AbstractUser):
    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.username

