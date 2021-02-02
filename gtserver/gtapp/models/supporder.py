from django.db import models
from gtapp.models.custorderdet import CustOrderDet
from . import Order, Supplier, CustOrder

class SuppOrder(Order):
    """
    Diese Model enthaelt die Kopfdaten der Lieferantenbestellungen.
    """   
    class Status(models.TextChoices):

        DEFAULT                 = '0', ('Standard')
        CAPTURED                = '1', ('Erfasst')
        INVENTORY_OUTSTANDING   = '2', ('Bestandsprüfung ausstehend')
        OUTSTANDING_DELIVERY    = '3', ('Lieferung an JOGA ausstehend')
        DELIVERED               = '4', ('Geliefert')
        ORDERED                 = '5', ("Bestellt")

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    
    status = models.CharField(
        max_length = 1,
        choices = Status.choices,
        default = Status.DEFAULT,
    )
    
    def __str__(self):
        return ("Bestellung " + self.order_no)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            #JOGA
            if self.external_system == False:
                mylist = list(SuppOrder.objects.filter(external_system = self.external_system).order_by('-id'))
                if not mylist:
                    no_str = 'B-001'
                else:
                    tmp = mylist[0].order_no
                    mytmp=tmp.split('-')
                    no = int(mytmp[1])
                    no = no+1
                    if (no<10):
                        no_str = 'B-00'+str(no)
                    elif(no<100):
                        no_str = 'B-0'+str(no)
                    elif(no<1000):
                        no_str = 'B-'+str(no)
                    else:
                        pass
            #Lieferanten        
            else:
                mylist = list(SuppOrder.objects.filter(external_system = self.external_system, supplier_id=self.supplier_id).order_by('-id'))
                if not mylist:
                    no_str = 'L' + str(self.supplier_id) +'-001'
                else:
                    #Bestimmung der neuen Orderno
                    tmp = mylist[0].order_no
                    mytmp=tmp.split('-')
                    no = int(mytmp[1])
                    no = no+1
                    if (no<10):
                        no_str =  'L' + str(self.supplier_id) +'-00'+str(no)
                    elif(no<100):
                        no_str = 'L' + str(self.supplier_id) +'-0'+str(no)
                    elif(no<1000):
                        no_str = 'L' + str(self.supplier_id) +str(no)
                    else:
                        pass
            self.order_no=no_str
        super(Order, self).save(*args, **kwargs)
    
    