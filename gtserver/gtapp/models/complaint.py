from django.db import models
from django.contrib.auth.models import User
from . import Status

class Complaint(models.Model):
    """
    This is an abstract template-Class for Supplier-Complaints and Customer-Complaints.
    It contains the fields, that all types of complaints have in common.
    """

    status = models.ForeignKey(Status,null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    memo = models.TextField()
    finished_on = models.SmallIntegerField()

    class Meta:
        abstract = True