from django.db import models
from gtapp.models.custorderdet import CustOrderDet
from . import Order, Supplier

class SuppOrder(Order):
    """
    This model contains information about the Supplier-Orders.
    It inherits most of its fields from the abstract Order-Class.
    """   

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)