from django.db import models
from . import OrderDet, SuppOrder, Part

class SuppOrderDet(OrderDet):
    """
    Dieses Model enthaelt die Positionsdaten einer Lieferantenbestellung.
    """    
    class Status(models.TextChoices):

        DEFAULT                = '0', ('Standard')
        ORDERED                = '1', ('Bestellt')
        DELIVERED              = '2', ('Geliefert')
        
    supp_order = models.ForeignKey(SuppOrder, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    
    status = models.CharField(
        max_length = 1,
        choices = Status.choices,
        default = Status.DEFAULT,
    )

    def __str__(self):
        return str(str(self.supp_order) + ": Teil: "+ str(self.part) )