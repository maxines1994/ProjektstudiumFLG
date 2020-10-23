from django.db import models
from . import Status

class Container(models.Model):
    """
    This is an abstract template-Class for Supplier-Containers and Customer-Containers.
    It contains the fields, that all types of containers have in common.
    """   

    status = models.ForeignKey(Status,null=True, on_delete=models.SET_NULL)
    barcode = models.CharField(max_length=8)
    delivery_date = models.SmallIntegerField()
    memo = models.TextField()

    class Meta:
        abstract = True