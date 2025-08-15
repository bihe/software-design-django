# Create your models here.
from django.db import models

from core.models import Customer

"""
    we are using the Customer model for authentication, so we need to use the AbstractUser model
    for this project, only add nullable fields to the customer,
    otherwise you could run into trouble with creating suerpusers.
"""


# this is the concrete model that we will use for the project
class Customer(Customer):
    class Meta:
        db_table: str = "customer"

    # we are adding a credit field to the customer model
    credit: float = models.FloatField(null=True)
