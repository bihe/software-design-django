# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

"""
    we are using the Customer model for authentication, so we need to use the AbstractUser model
    for this project, only add nullable fields to the customer,
    otherwise you could run into trouble with creating suerpusers.
"""


# this is the concrete model that we will use for the project
class Customer(AbstractUser):
    class Meta:
        db_table: str = "customer"

    # we are adding a credit field to the customer model
    credit: float = models.FloatField(null=True)

    # this is needed for Django Model-forms:
    # https://docs.djangoproject.com/en/5.2/topics/class-based-views/generic-editing/
    def get_absolute_url(self):
        return reverse("customers:customer-detail", kwargs={"pk": self.pk})
