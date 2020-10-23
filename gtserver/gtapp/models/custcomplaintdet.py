from django.db import models
from . import ComplaintDet, CustComplaint, CustOrderDet

class CustComplaintDet(ComplaintDet):
    """
    This model contains detailed information for every position of a Complaint from a Customer.
    Most fields are inherited from the abstract ComplaintDet-class.
    """
    cust_complaint = models.ForeignKey(CustComplaint, on_delete=models.CASCADE)
    cust_order_det = models.ForeignKey(CustOrderDet, on_delete=models.CASCADE)