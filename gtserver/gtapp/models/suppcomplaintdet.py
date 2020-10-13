from django.db import models
from . import Complaint, SuppComplaint, SuppOrderDet

"""
This model contains detailed information for every position of a Complaint towards a Supplier.
Most fields are inherited from the abstract ComplaintDet-class.
"""

class SuppComplaintDet(Complaint):
    SuppComplaint = models.ForeignKey(SuppComplaint, on_delete=models.CASCADE)
    SuppOrderDet = models.ForeignKey(SuppOrderDet, on_delete=models.CASCADE)