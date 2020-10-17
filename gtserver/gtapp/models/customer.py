from django.db import models
from . import Status

"""
This model contains master data of the costumers
"""

class Customer(models.Model):
    Status = models.ForeignKey(Status, on_delete=models.CASCADE)
    Name = models.CharField(max_length=30)
    Memo = models.TextField()