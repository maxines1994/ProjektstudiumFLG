from django.db import models
from django.contrib.auth.models import User
from . import Order, Customer

class CustOrder(Order):
    """
    This model contains information about the Costumer-Orders.
    It inherits most of its fields from the abstract Order-Class.
    """    

    costumer = models.ForeignKey(Customer, on_delete=models.CASCADE)