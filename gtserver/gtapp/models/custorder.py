from django.db import models
from django.contrib.auth.models import User
from . import Order, Customer

class CustOrder(Order):
    """
    Diese Model enthaelt die Kopfdaten der Kundenauftraege.
    """  
    class Status(models.TextChoices):

        ERFASST                             = 1, ('Erfasst|0%')
        TEILGELIEFERT                       = 2, ('Teilgeliefert|50%')
        GELIEFERT                           = 3, ('Geliefert|100%')
        
    
    status = models.CharField(
        max_length = 2,
        choices = Status.choices,
        default = Status.ERFASST,
    )

    def get_status_display(self):
        return self.Status(self.status).label.split("|", 1)[0]

    def get_status_progress(self):
        return self.Status(self.status).label.split("|", 1)[-1]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    #ref_no = models.ForeignKey(CustOrder, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.order_no

    def save(self, *args, **kwargs):
        if not self.pk:
            #JOGA
            if self.external_system == False:
                mylist = list(CustOrder.objects.filter(external_system = self.external_system).order_by('-id'))
                if not mylist:
                    no_str = 'A-001'
                else:
                    tmp = mylist[0].order_no
                    mytmp=tmp.split('-')
                    no = int(mytmp[1])
                    no = no+1
                    if (no<10):
                        no_str = 'A-00'+str(no)
                    elif(no<100):
                        no_str = 'A-0'+str(no)
                    else:
                        no_str = 'A-'+str(no)
            #Kunden        
            else:
                mylist = list(CustOrder.objects.filter(external_system = self.external_system, customer_id=self.customer_id).order_by('-id'))
                if not mylist:
                    no_str = 'K' + str(self.customer_id) +'-001'
                else:
                    #Bestimmung der neuen Orderno
                    tmp = mylist[0].order_no
                    mytmp=tmp.split('-')
                    no = int(mytmp[1])
                    no = no+1
                    if (no<10):
                        no_str =  'K' + str(self.customer_id) +'-00'+str(no)
                    elif(no<100):
                        no_str = 'K' + str(self.customer_id) +'-0'+str(no)
                    else:
                        no_str = 'K' + str(self.customer_id) +str(no)
            self.order_no=no_str
        super(Order, self).save(*args, **kwargs)
        