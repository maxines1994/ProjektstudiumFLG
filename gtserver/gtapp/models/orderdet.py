from django.db import models
from . import Status

"""
This is an abstract template-Class for Supplier-Order-Details and Customer-Order-Details.
It contains the fields, that all types of Order-Details have in common.
"""

class OrderDet(models.Model):
    Status = models.ForeignKey(Status,null=True, on_delete=models.SET_NULL)
    Pos = models.IntegerField()
    UnitPrice = models.IntegerField()
    ReceivedOn = models.SmallIntegerField()
    Memo = models.TextField()

    class Meta:
        abstract = True