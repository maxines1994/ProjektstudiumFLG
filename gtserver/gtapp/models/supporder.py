from django.db import models
from gtapp.models.custorderdet import CustOrderDet
from . import Order, Supplier, CustOrder

class SuppOrder(Order):
    """
    Diese Model enthaelt die Kopfdaten der Lieferantenbestellungen.
    """   
    class Status(models.TextChoices):

        ERFASST                         = 1, ('Erfasst|0%')
        BESTANDSPRUEFUNG_AUSSTEHEND     = 2, ('Bestandsprüfung ausstehend|20%')
        LIEFERUNG_AN_JOGA_AUSSTEHEND    = 3, ('Lieferung an JOGA ausstehend|40%')
        BESTELLT                        = 4, ("Bestellt|50%") ## Nur für JOGA, richtig?
        TEILGELIEFERT                   = 6, ("Teilgeliefert|70%")
        GELIEFERT                       = 7, ('Geliefert|100%')
        STORNIERT                       = 8, ('Storniert|100%')
        
    status = models.CharField(
        max_length = 2,
        choices = Status.choices,
        default = Status.ERFASST,
    )

    def get_status_display(self):
        return self.Status(self.status).label.split("|", 1)[0]

    def get_status_progress(self):
        return self.Status(self.status).label.split("|", 1)[-1]

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)



    def __str__(self):
        return self.order_no
    
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
                    else:
                        no_str = 'B-'+str(no)
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
                    else:
                        no_str = 'L' + str(self.supplier_id) +str(no)
            self.order_no=no_str
        super(Order, self).save(*args, **kwargs)
