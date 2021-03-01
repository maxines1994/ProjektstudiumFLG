from django.db import models
from .complaint import Complaint
from .custorder import CustOrder
from . import Customer
from gtapp.constants import *
from django.contrib.auth.models import Group

class CustComplaint(Complaint):
    """
    Dieses Model enthaelt die Kopfdaten von Kundenreklamationen
    """

    class Status(models.TextChoices):

        ERFASST                         = '0', ('Erfasst||0%')
        REKLAMATION_FREIGEGEBEN         = '1', ('Reklamation freigegeben||10%')
        IN_REKLAMATION                  = '2', ('In Reklamation||50%') ##Nur für den Kunden
        VERSAND_AN_PRODUKTION           = '3', ('Versandt an Produktion||20%')
        IN_ANPASSUNG                    = '4', ('In Anpassung||30%')
        ANPASSUNG_ABGESCHLOSSEN         = '5', ('Anpassung abgeschlossen||50%')
        VERSAND_AN_KUNDENDIENST         = '6', ('Versandt an Kundendienst||60%')
        BEI_KUNDENDIENST                = '7', ('Bereit zum Versand an Kunden||70%')
        VERSAND_AN_KUNDE                = '8', ('Versandt an Kunde||80%')
        GELIEFERT                       = '9', ('Geliefert||90%')
        ABGESCHLOSSEN                   = '10', ('Abgeschlossen||100%')

    status = models.CharField(
        max_length = 2,
        choices = Status.choices,
        default = Status.ERFASST,
    )

    cust_order = models.ForeignKey(CustOrder, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,null=True, on_delete=models.CASCADE)

    def get_status_display(self):
        return self.Status(self.status).label.split("|", 2)[0]

    def get_status_progress(self):
        return self.Status(self.status).label.split("|", 2)[-1]
    
    def group_has_work(self, user):
        from . import CustComplaintDet
        for det in CustComplaintDet.objects.filter(cust_complaint=self.pk):
            if det.group_has_work(user):
                return True
        return False

    def __str__(self):
        return self.order_no

    def save(self, *args, **kwargs):
        if not self.pk:
            #JOGA
            if self.external_system == False:
                mylist = list(CustComplaint.objects.filter(external_system = self.external_system).order_by('-id'))
                if not mylist:
                    no_str = 'RA-001'
                else:
                    tmp = mylist[0].order_no
                    mytmp=tmp.split('-')
                    no = int(mytmp[1])
                    no = no+1
                    if (no<10):
                        no_str = 'RA-00'+str(no)
                    elif(no<100):
                        no_str = 'RA-0'+str(no)
                    elif(no<1000):
                        no_str = 'RA-'+str(no)
                    else:
                        pass
            #Kunden , customer_id=self.cust_order.customer.pk        
            else:
                mylist = list(CustComplaint.objects.filter(external_system = self.external_system, customer_id=self.cust_order.customer.pk).order_by('-id'))
                if not mylist:
                    no_str = 'RK' + str(self.cust_order.customer.pk) +'-001'
                else:
                    #Bestimmung der neuen Orderno
                    tmp = mylist[0].order_no
                    mytmp=tmp.split('-')
                    no = int(mytmp[1])
                    no = no+1
                    if (no<10):
                        no_str = 'RK' + str(self.cust_order.customer.pk) +'-00'+str(no)
                    elif(no<100):
                        no_str = 'RK' + str(self.cust_order.customer.pk) +'-0'+str(no)
                    elif(no<1000):
                        no_str = 'RK' + str(self.cust_order.customer.pk) +str(no)
                    else:
                        pass

               
            self.order_no=no_str
        super(Complaint, self).save(*args, **kwargs)
