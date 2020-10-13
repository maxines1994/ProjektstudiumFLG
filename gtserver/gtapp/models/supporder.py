from django.db import models
from gtapp.models.custorderdet import CustOrderDet
from . import Order, Supplier

"""
This model contains information about the Supplier-Orders.
It inherits most of its fields from the abstract Order-Class.
"""

class SuppOrder(Order):
    Supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)