from django.db import models
from .complaint import Complaint
from .supporder import SuppOrder
from .supplier import Supplier


class SuppComplaint(Complaint):
    """
    Dieses Model enthaelt die Kopfdaten von Lieferanten-Reklamationen.
    """
    supp_order = models.ForeignKey(SuppOrder,on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE)