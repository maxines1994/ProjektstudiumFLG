from django.db import models
from . import Status

"""
This model contains master data of suppliers, that sell the parts which are needed to build lifting platforms.
"""

class Supplier(models.Model):
    Status = models.ForeignKey(Status,null=True, on_delete=models.SET_NULL)
    Name = models.CharField(max_length=30)
    Memo = models.TextField()
