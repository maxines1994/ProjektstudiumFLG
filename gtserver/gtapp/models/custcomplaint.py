from django.db import models
from .complaint import Complaint
from .custorder import CustOrder

class CustComplaint(Complaint):
    """
    Dieses Model enthaelt die Kopfdaten von Kundenreklamationen
    """
    cust_order = models.ForeignKey(CustOrder,on_delete=models.CASCADE)

