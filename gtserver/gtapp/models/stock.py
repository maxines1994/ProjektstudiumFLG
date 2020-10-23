from django.db import models
from . import Part

class Stock(models.Model):
    """
    This model contains information about the stock of each part.
    Stock is the current amount that is inside the warehouse.
    Reserved is the amount that is currently reserved for withdrawal for Supplier-Orders.
    """

    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    stock = models.SmallIntegerField()
    reserved = models.SmallIntegerField(default=0)