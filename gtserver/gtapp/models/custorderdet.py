from django.db import models
from django.apps import apps
from . import OrderDet, CustOrder, Article

class CustOrderDet(OrderDet):
    """
    Dieses Model enthaelt die Positionsdaten eines Kundenauftrages.
    """   
    class Status(models.TextChoices):

        DEFAULT                = '0', ('Standard')
        BEING_ORDERED          = '1', ('Wird bestellt')
        APPROVED               = '2', ('Freigegeben')
        IN_PROGRESS            = '3', ('In Bearbeitung')
        PROCESSING_COMPLETE    = '4', ('Bearbeitung abgeschlossen')
        BEING_PRODUCED         = '5', ('Wird produziert')
        DONE                   = '6', ('Produktion abgeschlossen')
        DELIVERED              = '7', ('Geliefert')
        COMPLAINED             = '8', ('Reklamiert')
        ACCEPTED               = '9', ('bgenommen')
    
    status = models.CharField(
        max_length = 1,
        choices = Status.choices,
        default = Status.DEFAULT,
    )

    
    cust_order = models.ForeignKey(CustOrder, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(str(self.cust_order) + ": Artikel: "+ str(self.article) )
