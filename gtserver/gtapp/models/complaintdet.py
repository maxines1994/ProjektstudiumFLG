from django.db import models

#Abstract Class for Complaint-Details that contains fields, that all types of complaint-detailss have in common.

class ComplaintDet(models.Model):
    Status = models.CharField(max_length=1)
    Pos = models.SmallIntegerField()
    Quantity = models.SmallIntegerField()
    Memo = models.TextField()

    class Meta:
        abstract = True