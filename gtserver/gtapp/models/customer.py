from django.db import models
from . import Status

class Customer(models.Model):
    """
    This model contains master data of the costumers
    """ 

    status = models.ForeignKey(Status,null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=30)
    memo = models.TextField(null=True)