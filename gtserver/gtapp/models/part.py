from django.db import models
from . import Status, Supplier

"""
This model contains information about the parts that make up a lifting platform.
They can be purchased from suppliers.
"""

class Part(models.Model):
   Status = models.ForeignKey(Status,null=True, on_delete=models.SET_NULL)
   PartNo = models.CharField(max_length=8)
   Description = models.CharField(max_length=30)
   UnitPrice = models.SmallIntegerField()
   Picture = models.BinaryField()
   Supplier = models.ForeignKey(Supplier, null=True, on_delete=models.SET_NULL)
   PackQuantity = models.SmallIntegerField()
