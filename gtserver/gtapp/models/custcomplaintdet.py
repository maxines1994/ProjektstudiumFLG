from django.db import models
from . import ComplaintDet, CustComplaint, CustOrderDet

"""
This model contains detailed information for every position of a Complaint from a Customer.
Most fields are inherited from the abstract ComplaintDet-class.
"""

class CustComplaintDet(ComplaintDet):
    CustComplaint = models.ForeignKey(CustComplaint, on_delete=models.CASCADE)
    CustOrderDet = models.ForeignKey(CustOrderDet, on_delete=models.CASCADE)