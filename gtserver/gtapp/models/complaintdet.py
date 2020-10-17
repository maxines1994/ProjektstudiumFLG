from django.db import models
from . import Status

"""
This is an abstract template-Class for Supplier-Complaint-Details and Customer-Complaint-Details.
It contains the fields, that all types of complaint-details have in common.
"""

class ComplaintDet(models.Model):
    Status = models.ForeignKey(Status, on_delete=models.CASCADE)
    Pos = models.SmallIntegerField()
    Quantity = models.SmallIntegerField()
    Memo = models.TextField()

    class Meta:
        abstract = True