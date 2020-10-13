from django.db import models
from . import Part

"""
This model contains information about the stock of each part.
Stock is the current amount that is inside the warehouse.
Reserved is the amount that is currently reserved for withdrawal for Supplier-Orders.
"""

class Stock(models.Model):
    PartID = models.ForeignKey(Part, on_delete=models.CASCADE)
    Stock = models.SmallIntegerField()
    Reserved = models.SmallIntegerField()