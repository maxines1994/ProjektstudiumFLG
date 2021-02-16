from django.db import models
from django.apps import apps
from . import OrderDet, CustOrder, Article, ArtiPart

class CustOrderDet(OrderDet):
    """
    Dieses Model enthaelt die Positionsdaten eines Kundenauftrages.
    """ 
    class Status(models.TextChoices):

        ERFASST                             = '1', ('Erfasst|0%')
        BESTANDSPRUEFUNG_AUSSTEHEND         = '2', ('Bestandsprüfung ausstehend|10%')
        AUFTRAG_FREIGEGEBEN                 = '3', ('Auftrag freigegeben|20%')
        IN_PRODUKTION                       = '4', ('In Produktion|30%')
        LIEFERUNG_AN_KD_AUSSTEHEND          = '5', ('Produktion abgeschlossen|50%')
        VERSANDT_AN_KD                      = '6', ('An Kundendienst versandt|60%')
        LIEFERUNG_AN_K_AUSSTEHEND           = '7', ('Lieferung an Kunden ausstehend|70%')
        BESTELLT                            = '8', ('Bestellt|30%')                       # für Kundensystem
        VERSANDT_AN_K                       = '9', ('Versandt|80%')
        GELIEFERT                           = '10', ('Geliefert|90%')
        REKLAMIERT                          = '11', ('Reklamiert|100%')
        ABGENOMMEN                          = '12', ('Abgenommen|100%')
        STORNIERT                           = '13', ('Storniert|100%')

    status = models.CharField(
        max_length = 2,
        choices = Status.choices,
        default = Status.ERFASST,
    )

    def get_status_display(self):
        return self.Status(self.status).label.split("|", 1)[0]

    def get_status_progress(self):
        return self.Status(self.status).label.split("|", 1)[-1]

    cust_order = models.ForeignKey(CustOrder, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.pos.__str__()

    def auto_needs(self):
        needs = list()
        atpt = ArtiPart.objects.filter(article_id=self.article.id, part__supplier_id=3)
        for p in atpt:
            needs.append((p.part, p.quantity))
        return needs

    def get_artiparts(self, supplier_ids=[1,2,3]):
        """
        Gibt die ArtiPart-Datensaetze zurueck, die zum Artikel dieser CustOrderDet gehoeren.
        Kann optional auf supplier mittels ID-Liste eingeschrankt werden.
        """
        return ArtiPart.objects.filter(article_id=self.article.id, part__supplier_id__in=supplier_ids)
    

# Liste der Fertigungsaufträge-Berechtigung
# Django bietet custom Permissions, diese würden aber nicht mit unserer Migration funktionieren, daher ein Model als simpler Workaround
class PermManufacturingList(models.Model):
    pass