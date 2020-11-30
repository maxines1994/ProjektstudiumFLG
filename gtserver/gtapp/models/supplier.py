from django.db import models
from . import Status

class Supplier(models.Model):
    """
    This model contains master data of suppliers, that sell the parts which are needed to build lifting platforms.
    """

    status = models.ForeignKey(Status,null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=30)
    memo = models.TextField()
