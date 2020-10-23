from django.db import models
from . import Complaint, SuppComplaint, SuppOrderDet

class SuppComplaintDet(Complaint):
    """
    This model contains detailed information for every position of a Complaint towards a Supplier.
    Most fields are inherited from the abstract ComplaintDet-class.
    """    

    supp_complaint = models.ForeignKey(SuppComplaint, on_delete=models.CASCADE)
    supp_order_det = models.ForeignKey(SuppOrderDet, on_delete=models.CASCADE)