from django.db import models
from . import Status

class OrderDet(models.Model):
    """
    This is an abstract template-Class for Supplier-Order-Details and Customer-Order-Details.
    It contains the fields, that all types of Order-Details have in common.
    """
    status = models.ForeignKey(Status,null=True, on_delete=models.SET_NULL)
    pos = models.IntegerField()
    unit_price = models.IntegerField()
    received_on = models.SmallIntegerField()
    memo = models.TextField()

    class Meta:
        abstract = True