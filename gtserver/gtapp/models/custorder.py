from django.db import models
from django.contrib.auth.models import User
from . import Order, Customer

class CustOrder(Order):
    """
    Diese Model enthaelt die Kopfdaten der Kundenauftraege.
    """    

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    #ref_no = models.ForeignKey(CustOrder, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return ("Auftrag " + self.order_no)

    def save(self, *args, **kwargs):
        if not self.pk:
            mylist = list(CustOrder.objects.filter(external_system = self.external_system).order_by('-id'))
            print("PRINT:" + str(self.external_system))
            if self.external_system == 0:
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
                    elif(no<1000):
                        no_str = 'A-'+str(no)
                    else:
                        pass
            else:
                if not mylist:
                    no_str = 'B-001'
                else:
                    tmp = mylist[0].order_no
                    mytmp=tmp.split('-')
                    no = int(mytmp[1])
                    no = no+1
                    if (no<10):
                        no_str = self.user.user_name +'-00'+str(no)
                    elif(no<100):
                        no_str = 'K1-0'+str(no)
                    elif(no<1000):
                        no_str = 'K1-'+str(no)
                    else:
                        pass
            self.order_no=no_str
        super(Order, self).save(*args, **kwargs)