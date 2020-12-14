from django.db import models
from . import OrderDet, SuppOrder, Part

class SuppOrderDet(OrderDet):
    """
    Dieses Model enthaelt die Positionsdaten einer Lieferantenbestellung.
    """    

    supp_order = models.ForeignKey(SuppOrder, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()