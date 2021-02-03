from django.db import models
from django.apps import apps
from . import OrderDet, CustOrder, Article, ArtiPart

class CustOrderDet(OrderDet):
    """
    Dieses Model enthaelt die Positionsdaten eines Kundenauftrages.
    """   
    class Status(models.TextChoices):

        STANDARD                            = '0', ('Standard')
        ERFASST                             = '1', ('Erfasst')
        BESTANDSPRUEFUNG_AUSSTEHEND         = '2', ('Bestandsprüfung ausstehend')
        AUFTRAG_FREIGEGEBEN                 = '3', ('Auftrag freigegeben')
        IN_PRODUKTION                       = '4', ('In Produktion')
        LIEFERUNG_AN_KD_AUSSTEHEND          = '5', ('Lieferung an Kundendienst ausstehend')
        LIEFERUNG_AN_K_AUSSTEHEND           = '6', ('Lieferung an Kunden ausstehend')
        BESTELLT                            = '7', ('Bestellt') # für Kundensystem
        GELIEFERT                           = '8', ('Geliefert')
        REKLAMIERT                          = '9', ('Reklamiert')
        
    
    status = models.CharField(
        max_length = 1,
        choices = Status.choices,
        default = Status.STANDARD,
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
