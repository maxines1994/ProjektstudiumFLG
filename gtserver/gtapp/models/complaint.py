from django.db import models
from django.contrib.auth.models import User

"""
This is an abstract template-Class for Supplier-Complaints and Customer-Complaints.
It contains the fields, that all types of complaints have in common.
"""

class Complaint(models.Model):
    Status = models.CharField(max_length=1)
    User = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    Memo = models.TextField()
    FinishedOn = models.SmallIntegerField()

    class Meta:
        abstract = True