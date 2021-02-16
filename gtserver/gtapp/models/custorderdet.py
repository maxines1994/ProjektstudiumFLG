from django.db import models
from django.apps import apps
from . import OrderDet, CustOrder, Article, ArtiPart

class CustOrderDet(OrderDet):
    """
    Dieses Model enthaelt die Positionsdaten eines Kundenauftrages.
    """ 
    class Status(models.TextChoices):
        
        # ERFASST
        ERFASST                             = '1', ('Erfasst|0%') # auch für Kundensystem

        # FREIGEGEBEN
        BESTANDSPRUEFUNG_AUSSTEHEND         = '2', ('Bestandsprüfung ausstehend|10%')
        BESTANDSPRUEFUNG_ABGESCHLOSSEN      = '3', ('Bestandsprüfung abgeschlossen|15%')
        AUFTRAG_FREIGEGEBEN                 = '4', ('Auftrag freigegeben|20%') 

        # IN BEARBEITUNG
        IN_PRODUKTION                       = '5', ('In Produktion|30%')
        LIEFERUNG_AN_KD_AUSSTEHEND          = '6', ('Produktion abgeschlossen|50%')
        VERSANDT_AN_KD                      = '7', ('An Kundendienst versandt|60%')
        LIEFERUNG_AN_K_AUSSTEHEND           = '8', ('Lieferung an Kunden ausstehend|70%')

        # BESTELLT, nur Kunde
        BESTELLT                            = '9', ('Bestellt|30%')                       # für Kundensystem only

        # TEILGELIEFERT
        VERSANDT_AN_K                       = '10', ('Versandt|90%')
        # GELIEFERT - MINSTATUS GELIEFERT (aka alle geliefert)
        GELIEFERT                           = '11', ('Geliefert|90%') # für Kundensystem only

        # ABGENOMMEN
        ABGENOMMEN                          = '13', ('Abgenommen|100%') # auch für Kundensystem

        # STORNIERT
        STORNIERT                           = '14', ('Storniert|100%')

    status = models.CharField(
        max_length = 2,
        choices = Status.choices,
        default = Status.ERFASST,
    )

    def get_min_status(self):
        # here to avoid import loop
        minstatus = 9000
        for i in CustOrderDet.objects.filter(cust_order=self.cust_order.pk):
            if int(i.status) < minstatus:
                minstatus = int(i.status)
        return minstatus

    def save(self, *args, **kwargs):

        # Status auf Kopfebene setzen
        # Normale Status
        minstatus = self.get_min_status()

        if self.cust_order.external_system == False:
            # JOGA
            if minstatus <= int(self.Status.ERFASST):
                self.cust_order.status = CustOrder.Status.ERFASST

            elif minstatus <= int(self.Status.AUFTRAG_FREIGEGEBEN):
                self.cust_order.status = CustOrder.Status.FREIGEGEBEN

            elif minstatus <= int(self.Status.LIEFERUNG_AN_K_AUSSTEHEND):
                # Wenn schon Positionen geliefert wurden teilgeliefert, sonst in Bearbeitung
                if CustOrderDet.objects.filter(status=self.Status.GELIEFERT).exists():
                    self.cust_order.status = CustOrder.Status.TEILGELIEFERT
                else:
                    self.cust_order.status = CustOrder.Status.IN_BEARBEITUNG

            elif minstatus <= int(self.Status.GELIEFERT):
                self.cust_order.status = CustOrder.Status.GELIEFERT

            elif minstatus <= int(self.Status.ABGENOMMEN):
                self.cust_order.status = CustOrder.Status.ABGENOMMEN

            elif minstatus <= int(self.Status.STORNIERT):
                self.cust_order.status = CustOrder.Status.STORNIERT

            else:
                # Fallback
                self.cust_order.status = CustOrder.Status.ERFASST
        else:
            # Kundensystem
            if minstatus <= int(self.Status.ERFASST):
                self.cust_order.status = CustOrder.Status.ERFASST

            elif minstatus <= int(self.Status.BESTELLT):
                # Wenn schon Positionen geliefert wurden teilgeliefert, sonst in Bearbeitung
                if CustOrderDet.objects.filter(status=self.Status.GELIEFERT).exists():
                    self.cust_order.status = CustOrder.Status.TEILGELIEFERT
                else:
                    self.cust_order.status = CustOrder.Status.BESTELLT

            elif minstatus <= int(self.Status.GELIEFERT):
                self.cust_order.status = CustOrder.Status.GELIEFERT

            elif minstatus <= int(self.Status.ABGENOMMEN):
                self.cust_order.status = CustOrder.Status.ABGENOMMEN

            elif minstatus <= int(self.Status.STORNIERT):
                self.cust_order.status = CustOrder.Status.STORNIERT

            else:
                # Fallback
                self.cust_order.status = CustOrder.Status.ERFASST

        self.cust_order.save()
        
        super(CustOrderDet, self).save(*args, **kwargs)

    def get_status_display(self):
        return self.Status(self.status).label.split("|", 1)[0]

    def get_status_progress(self):
        return self.Status(self.status).label.split("|", 1)[-1]

    cust_order = models.ForeignKey(CustOrder, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.pos.__str__() + ' ' + self.article.description

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