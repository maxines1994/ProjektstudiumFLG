from django.db import models
from . import Status

class ComplaintDet(models.Model):
    """
    This is an abstract template-Class for Supplier-Complaint-Details and Customer-Complaint-Details.
    It contains the fields, that all types of complaint-details have in common.
    """

    status = models.ForeignKey(Status,null=True, on_delete=models.SET_NULL)
    pos = models.SmallIntegerField()
    quantity = models.SmallIntegerField()
    memo = models.TextField()

    class Meta:
        abstract = True