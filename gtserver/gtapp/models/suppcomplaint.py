from django.db import models
from .complaint import Complaint
from .supporder import SuppOrder, Supplier


class SuppComplaint(Complaint):
    """
    Dieses Model enthaelt die Kopfdaten von Lieferanten-Reklamationen.
    """
    class Status(models.TextChoices):

        STANDARD                        = '0', ('Standard')
        ERFASST                         = '1', ('Erfasst')
        IN_REKLAMATION                  = '2', ('In Reklamation') ##Nur für den Lieferanten
        BEI_PDL                         = '3', ('Bei PDL') ##Nur wenn Rekla in PRO erstellt
        REKLAMIERT                      = '4', ('Reklamiert')
        BESTANDSPRUEFUNG_AUSSTEHEND     = '5', ('Bestandsprüfung ausstehend')
        LIEFERUNG_AN_PDL                = '6', ('Lieferung an PDL')
        GELIEFERT                       = '7', ('Geliefert')
        ABGESCHLOSSEN                   = '8', ('Abgeschlossen') ##Nur wenn keine Neulieferung

    status = models.CharField(
        max_length = 1,
        choices = Status.choices,
        default = Status.ERFASST,
    )

    supp_order = models.ForeignKey(SuppOrder, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, null=True,on_delete=models.CASCADE)


    def __str__(self):
        return ("Bestellung " + self.order_no)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            #JOGA
            if self.external_system == False:
                mylist = list(SuppComplaint.objects.filter(external_system = self.external_system).order_by('-id'))
                if not mylist:
                    no_str = 'RB-001'
                else:
                    tmp = mylist[0].order_no
                    mytmp=tmp.split('-')
                    no = int(mytmp[1])
                    no = no+1
                    if (no<10):
                        no_str = 'RB-00'+str(no)
                    elif(no<100):
                        no_str = 'RB-0'+str(no)
                    elif(no<1000):
                        no_str = 'RB-'+str(no)
                    else:
                        pass
            #Lieferanten        
            else:
                mylist = list(SuppComplaint.objects.filter(external_system = self.external_system, supplier_id=self.supplier_id).order_by('-id'))
                if not mylist:
                    no_str = 'RL' + str(self.supplier_id) +'-001'
                else:
                    #Bestimmung der neuen Orderno
                    tmp = mylist[0].order_no
                    mytmp=tmp.split('-')
                    no = int(mytmp[1])
                    no = no+1
                    if (no<10):
                        no_str =  'RL' + str(self.supplier_id) +'-00'+str(no)
                    elif(no<100):
                        no_str = 'RL' + str(self.supplier_id) +'-0'+str(no)
                    elif(no<1000):
                        no_str = 'RL' + str(self.supplier_id) +str(no)
                    else:
                        pass
            self.order_no=no_str
        super(Complaint, self).save(*args, **kwargs)
