from django.db import models
from django.apps import apps
from . import OrderDet, CustOrder, Article

class CustOrderDet(OrderDet):
    """
    Dieses Model enthaelt die Positionsdaten eines Kundenauftrages.
    """   
    class Status(models.TextChoices):

        DEFAULT                 =  '0',('Standard')
        CAPTURED                 = '1', ('Erfasst')
        INVENTORY                = '2', ('Bestandsprüfung ausstehend')
        ORDER_RELEASE            = '3', ('Auftrag freigegeben')
        IN_PRODUCTION            = '4', ('In Produktion')
        DELIVERY_KD              = '5', ('Lieferung an Kundendienst ausstehend')
        DELIVERY_CUST            = '6', ('Lieferung an Kunden ausstehend')
        DELIVERED                = '7', ('Geliefert')
        COMPLAINED               = '8', ('Reklamiert')
        #Kundensystem Erfasst - Bestellt - Geliefert
        ACCEPTED                 = '9', ('Bestellt')
    
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
