from django.db import models
from . import OrderDet, SuppOrder, Part

"""
This model contains detailed information for every position of a Supplier-Order.
It inherits most of its fields from the abstract OrderDet-Class.
"""

class SuppOrderDet(OrderDet):
    SuppOrder = models.ForeignKey(SuppOrder, on_delete=models.CASCADE)
    Part = models.ForeignKey(Part, on_delete=models.CASCADE)