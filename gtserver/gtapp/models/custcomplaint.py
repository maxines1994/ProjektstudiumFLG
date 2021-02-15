from django.db import models
from .complaint import Complaint
from .custorder import CustOrder
from . import Customer

class CustComplaint(Complaint):
    """
    Dieses Model enthaelt die Kopfdaten von Kundenreklamationen
    """

    class Status(models.TextChoices):

        ERFASST                         = '0', ('Erfasst')
        REKLAMATION_FREIGEGEBEN         = '1', ('Reklamation freigegeben')
        IN_REKLAMATION                  = '2', ('In Reklamation') ##Nur für den Kunden
        VERSAND_AN_PRODUKTION           = '3', ('Versand an Produktion')
        IN_ANPASSUNG                    = '4', ('In Anpassung')
        ANPASSUNG_ABGESCHLOSSEN         = '5', ('Anpassung abgeschlossen')
        VERSAND_AN_KUNDENDIENST         = '6', ('Versand an Kundendienst')
        BEI_KUNDENDIENST                = '7', ('Bei Kundendienst')
        VERSAND_AN_KUNDE                = '8', ('Versand an Kunde')
        GELIEFERT                       = '9', ('Geliefert')
        ABGESCHLOSSEN                   = '10', ('Abgeschlossen')

    status = models.CharField(
        max_length = 2,
        choices = Status.choices,
        default = Status.ERFASST,
    )

    cust_order = models.ForeignKey(CustOrder, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,null=True, on_delete=models.CASCADE)

    def __str__(self):
        return (self.order_no)

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
