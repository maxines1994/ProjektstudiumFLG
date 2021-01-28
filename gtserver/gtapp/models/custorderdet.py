from django.db import models
from django.apps import apps
from . import OrderDet, CustOrder, Article

class CustOrderDet(OrderDet):
    """
    Dieses Model enthaelt die Positionsdaten eines Kundenauftrages.
    """   
    class Status(models.TextChoices):

        DEFAULT                = '0', ('Standard')
        BEING_ORDERED          = '1', ('Bestandsreservierung ausstehend')
        APPROVED               = '2', ('Freigegeben')
        IN_PROGRESS            = '3', ('Materialbereitstellung ausstehend')
        BEING_PRODUCED         = '4', ('Wird produziert')
        DONE                   = '5', ('Lieferung an Kundendienst ausstehend')
        DELIVERED              = '6', ('Lieferung an Kunden ausstehend')
        ACCEPTED               = '7', ('Geliefert')
        
    status = models.CharField(
        max_length = 1,
        choices = Status.choices,
        default = Status.DEFAULT,
    )

    cust_order = models.ForeignKey(CustOrder, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.article)

    def auto_needs(self):
        needs = list()
        atpt = ArtiPart.objects.filter(article_id=self.article.id, part__supplier_id=3)
        for p in atpt:
            needs.append((p.part, p.quantity))
        return needs
