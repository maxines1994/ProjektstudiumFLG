from django.db import models
from django.contrib.auth.models import User
from . import Order, Customer

"""
This model contains information about the Costumer-Orders.
It inherits most of its fields from the abstract Order-Class.
"""

class CustOrder(Order):
    Costumer = models.ForeignKey(Customer, on_delete=models.CASCADE)