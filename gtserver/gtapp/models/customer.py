from django.db import models

"""
This model contains master data of the costumers
"""

class Customer(models.Model):
    Status = models.CharField(max_length=1)
    Name = models.CharField(max_length=30)
    Memo = models.TextField()