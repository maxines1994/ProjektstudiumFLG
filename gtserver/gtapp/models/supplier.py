from django.db import models

"""
This model contains master data of suppliers, that sell the parts which are needed to build lifting platforms.
"""

class Supplier(models.Model):
    Status = models.CharField(max_length=1)
    Name = models.CharField(max_length=30)
    Memo = models.TextField()
