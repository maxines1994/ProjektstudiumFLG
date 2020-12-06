from django.db import models
from . import Complaint, SuppComplaint, SuppOrderDet

class SuppComplaintDet(Complaint):
    """
    Diese Model enthaelt die Positionsdaten je Lieferanten-Reklamation.
    """    

    supp_complaint = models.ForeignKey(SuppComplaint, on_delete=models.CASCADE)
    supp_order_det = models.ForeignKey(SuppOrderDet, on_delete=models.CASCADE)