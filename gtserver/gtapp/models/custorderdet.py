from django.db import models
from django.apps import apps
from . import OrderDet, CustOrder, Article, ArtiPart

class CustOrderDet(OrderDet):
    """
    Dieses Model enthaelt die Positionsdaten eines Kundenauftrages.
    """ 
    class Status(models.TextChoices):

        ERFASST                             = '1', ('Erfasst|0%') # auch für Kundensystem
        BESTANDSPRUEFUNG_AUSSTEHEND         = '2', ('Bestandsprüfung ausstehend|10%')
        BESTANDSPRUEFUNG_ABGESCHLOSSEN      = '3', ('Bestandsprüfung abgeschlossen|15%')
        AUFTRAG_FREIGEGEBEN                 = '4', ('Auftrag freigegeben|20%')
        IN_PRODUKTION                       = '5', ('In Produktion|30%')
        LIEFERUNG_AN_KD_AUSSTEHEND          = '6', ('Produktion abgeschlossen|50%')
        VERSANDT_AN_KD                      = '7', ('An Kundendienst versandt|60%')
        LIEFERUNG_AN_K_AUSSTEHEND           = '8', ('Lieferung an Kunden ausstehend|70%')
        BESTELLT                            = '9', ('Bestellt|30%')                       # für Kundensystem only
        VERSANDT_AN_K                       = '10', ('Versandt|90%')
        GELIEFERT                           = '11', ('Geliefert|90%') # für Kundensystem only
        ABGENOMMEN                          = '13', ('Abgenommen|100%') # auch für Kundensystem
        STORNIERT                           = '14', ('Storniert|100%')

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