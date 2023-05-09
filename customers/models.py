
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import Customer

"""
    we are using the Customer model for authentication, so we need to use the AbstractUser model
    for this project, only add nullable fields to the customer,
    otherwise you could run into trouble with creating suerpusers.
    
"""


#class Customer(AbstractUser):
#    credit: float = models.FloatField(null=True)

class CustomerBase(Customer):
    class Meta:
        swappable: str = "CUSTOMER_MODEL"
        db_table: str = "customer_base"


class Customer(CustomerBase):
    class Meta:
        db_table: str = "customer_concrete"

    credit: float = models.FloatField()
