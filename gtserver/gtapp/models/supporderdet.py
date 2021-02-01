from django.db import models
from . import OrderDet, SuppOrder, Part

class SuppOrderDet(OrderDet):
    """
    Dieses Model enthaelt die Positionsdaten einer Lieferantenbestellung.
    """    
       
    supp_order = models.ForeignKey(SuppOrder, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    
    

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
