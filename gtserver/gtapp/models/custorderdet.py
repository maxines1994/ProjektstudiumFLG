from django.db import models
from django.apps import apps
from . import OrderDet, CustOrder, Article, ArtiPart

class CustOrderDet(OrderDet):
    """
    Dieses Model enthaelt die Positionsdaten eines Kundenauftrages.
    """ 
    class Status(models.TextChoices):

        ERFASST                             = '1', ('Erfasst')
        BESTANDSPRUEFUNG_AUSSTEHEND         = '2', ('Bestandsprüfung ausstehend')
        AUFTRAG_FREIGEGEBEN                 = '3', ('Auftrag freigegeben')
        IN_PRODUKTION                       = '4', ('In Produktion')
        LIEFERUNG_AN_KD_AUSSTEHEND          = '5', ('Produktion abgeschlossen')
        VERSANDT_AN_KD                      = '6', ('An Kundendienst versandt')
        LIEFERUNG_AN_K_AUSSTEHEND           = '7', ('Lieferung an Kunden ausstehend')
        BESTELLT                            = '8', ('Bestellt')                       # für Kundensystem
        VERSANDT_AN_K                       = '9', ('Versandt')
        GELIEFERT                           = '10', ('Geliefert')
        REKLAMIERT                          = '11', ('Reklamiert')
        ABGENOMMEN                          = '12', ('Abgenommen')
        STORNIERT                           = '13', ('Storniert')
        
    
    status = models.CharField(
        max_length = 2,
        choices = Status.choices,
        default = Status.ERFASST,
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

    def part_demand(self):
        return ArtiPart.objects.filter(article_id=self.article.id, part__supplier_id=3)




# Liste der Fertigungsaufträge-Berechtigung
# Django bietet custom Permissions, diese würden aber nicht mit unserer Migration funktionieren, daher ein Model als simpler Workaround
class PermManufacturingList(models.Model):
    pass