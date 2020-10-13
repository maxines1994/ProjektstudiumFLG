from django.db import models

"""
This is an abstract template-Class for Supplier-Containers and Customer-Containers.
It contains the fields, that all types of containers have in common.
"""

class Container(models.Model):
    Status = models.CharField(max_length=1)
    Barcode = models.CharField(max_length=8)
    DeliveryDate = models.SmallIntegerField()
    Memo = models.TextField()

    class Meta:
        abstract = True