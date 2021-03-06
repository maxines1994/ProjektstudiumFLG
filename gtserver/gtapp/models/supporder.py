from django.db import models
from gtapp.models.custorderdet import CustOrderDet
from . import Order, Supplier, CustOrder
from gtapp.constants import *
from django.contrib.auth.models import Group

class SuppOrder(Order):
    """
    Diese Model enthaelt die Kopfdaten der Lieferantenbestellungen.
    """   
    class Status(models.TextChoices):

        ERFASST                         = 1, ('Erfasst|' + PRODUKTIONSDIENSTLEISTUNG + ',' + LIEFERANTEN + '|0%')
        BESTANDSPRUEFUNG_AUSSTEHEND     = 2, ('Bestandsprüfung ausstehend|' + LIEFERANTEN + '|20%')
        LIEFERUNG_AN_JOGA_AUSSTEHEND    = 3, ('Lieferung an JOGA ausstehend|' + LIEFERANTEN + '|40%')
        BESTELLT                        = 4, ('Bestellt||50%') ## Nur für JOGA, richtig?
        TEILGELIEFERT                   = 6, ('Teilgeliefert|' + PRODUKTIONSDIENSTLEISTUNG + ',' + LIEFERANTEN + '|70%')
        GELIEFERT                       = 7, ('Geliefert||100%')
        STORNIERT                       = 8, ('Storniert||100%')
        
    status = models.CharField(
        max_length = 2,
        choices = Status.choices,
        default = Status.ERFASST,
    )

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def get_status_display(self):
        return self.Status(self.status).label.split("|", 2)[0]

    def get_status_progress(self):
        return self.Status(self.status).label.split("|", 2)[-1]
    
    def group_has_work(self, user):
        for group in Group.objects.filter(name__in=self.Status(self.status).label.split("|", 2)[1].split(',')):
            if user.groups.filter(name=group).exists():
                return True
        return False

    def __str__(self):
        return self.order_no
    
    def save(self, *args, **kwargs):
        masterdata=0
        if not self.pk:
            #JOGA
            if self.external_system == False:
                mylist = list(SuppOrder.objects.filter(external_system = self.external_system).order_by('-id'))
                if len(mylist) <3:
                    masterdata=1
                elif len(mylist) == 3:
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
                länge = len(mylist)
                
                if len(mylist) < 1:
                    masterdata=1
                elif len(mylist) == 1:
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
           
            if masterdata ==1:
                pass
            else:
                self.order_no=no_str
        super(Order, self).save(*args, **kwargs)
