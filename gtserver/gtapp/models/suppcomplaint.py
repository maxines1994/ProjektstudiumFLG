from django.db import models
from .complaint import Complaint
from .supporder import SuppOrder, Supplier
from gtapp.constants import *
from django.contrib.auth.models import Group

class SuppComplaint(Complaint):
    """
    Dieses Model enthaelt die Kopfdaten von Lieferanten-Reklamationen.
    """
    class Status(models.TextChoices):

        ERFASST                         = '0', ('Erfasst|0%')
        VERSAND_AN_PDL                  = '1', ('Versandt an PDL|10%')
        IN_BEARBEITUNG                  = '2', ('In Bearbeitung|20%')
        REKLAMATION_FREIGEGEBEN         = '3', ('Reklamation freigegeben|30%')
        BESTANDSPRUEFUNG_ABGESCHLOSSEN  = '4', ('Bestandsprüfung abgeschlossen|33%')##Nur LF
        VERSAND_AN_KUNDE                = '5', ('Versandt an Kunde|67%')##Nur LF
        AUS_LAGER_GELIEFERT             = '6', ('Aus Lager beliefert|40%')
        NEU_BESTELLEN                   = '7', ('Teil(e) neu bestellen|50%')
        POSITIONSBEARBEITUNG_FERTIG     = '8', ('Positionsbearbeitung fertig|60%')
        VERSAND_AN_LIEFERANT            = '9', ('Versandt an Lieferant|70%')
        GELIEFERT                       = '10', ('Geliefert|80%')
        VERSAND_AN_PRODUKTION           = '11', ('Versandt an Produktion|90%')
        ABGESCHLOSSEN                   = '12', ('Abgeschlossen|100%')   

    status = models.CharField(
        max_length = 2,
        choices = Status.choices,
        default = Status.ERFASST,
    )

    supp_order = models.ForeignKey(SuppOrder, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, null=True,on_delete=models.CASCADE)

    def get_status_display(self):
        return self.Status(self.status).label.split("|", 2)[0]

    def get_status_progress(self):
        return self.Status(self.status).label.split("|", 2)[-1]
    
    def group_has_work(self, user):
        from . import SuppComplaintDet
        for det in SuppComplaintDet.objects.filter(supp_complaint=self.pk):
            if det.group_has_work(user):
                return True
        return False

    def __str__(self):
        return self.order_no
    
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
