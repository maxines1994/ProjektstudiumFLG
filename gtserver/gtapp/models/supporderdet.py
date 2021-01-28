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
        return str(self.part.description)

    @classmethod
    def create_from_needs(cls, supp_order, needs=list()):
        for i in needs:
            p, q = i
            pt = Part.objects.filter(pk=p)[0]
            qtty=0
            o = q % pt.pack_quantity
            if o != 0:
                qtty = q-o+pt.pack_quantity
            else:
                qtty = q
