from django.db import models
from . import OrderDet, SuppOrder, Part, Timers

class SuppOrderDet(OrderDet):
    """
    Dieses Model enthaelt die Positionsdaten einer Lieferantenbestellung.
    """    
       
    supp_order = models.ForeignKey(SuppOrder, null=True, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()

    def __str__(self):
        return self.pos.__str__() + " " + self.part.description

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

    def auto_order(part_list:list, quantity_list:list):
        """
        Erwartet Listen von Teilen und Mengen und erzeugt daraus eine neue Bestellung
        mit entsprechenden Positionen. Gibt die ID der erstellten Bestellung zurueck
        """
        delivery_date = Timers.get_current_day() + 3
        new_supporder = SuppOrder.objects.create(supplier_id=3, delivery_date=delivery_date, issued_on=Timers.get_current_day(), memo="Automatisch generiert")
        list_length = len(part_list)
        # Packe die Listen zusammen. Die erste Liste ist ein Iterator von 1 bis zur Listenlaenge.
        # Es muss nochmal + 1 addiert werden, weil wir die 0 nicht mitzaehlen
        part_quantity = zip(range(1,list_length +1), part_list, quantity_list)
        for i, part, quantity in part_quantity:
            SuppOrderDet.objects.create(supp_order=new_supporder, pos=i, part_id=part, quantity=quantity)

        return new_supporder.id