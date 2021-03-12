from django.db import models
from django.apps import apps
from . import OrderDet, CustOrder, Article, ArtiPart
from gtapp.constants import *
from django.contrib.auth.models import Group

class CustOrderDet(OrderDet):
    """
    Dieses Model enthaelt die Positionsdaten eines Kundenauftrages.
    """ 
    class Status(models.TextChoices):
        
        # ERFASST
        ERFASST                             = '1', ('Erfasst|' + KUNDEN + ',' + KUNDENDIENST + '|0%') # auch für Kundensystem #K, KD

        # FREIGEGEBEN
        BESTANDSPRUEFUNG_AUSSTEHEND         = '2', ('Freigegeben|' + PRODUKTIONSDIENSTLEISTUNG + '|10%') #PDL
        BESTANDSPRUEFUNG_ABGESCHLOSSEN      = '3', ('Teile reserviert|' + PRODUKTIONSDIENSTLEISTUNG + '|15%')
        AUFTRAG_FREIGEGEBEN                 = '4', ('Kommissioniert||20%') 

        # IN BEARBEITUNG
        IN_PRODUKTION                       = '5', ('In Produktion|' + PRODUKTION + '|30%')
        LIEFERUNG_AN_KD_AUSSTEHEND          = '6', ('Produktion abgeschlossen|' + PRODUKTION + '|50%') #PRO
        VERSANDT_AN_KD                      = '7', ('An Kundendienst versandt|' + KUNDENDIENST + '|60%') #KD
        LIEFERUNG_AN_K_AUSSTEHEND           = '8', ('Bereit zum Versand an Kunden|' + KUNDENDIENST + '|70%') #KD

        # BESTELLT, nur Kunde
        BESTELLT                            = '9', ('Bestellt||30%') # für Kundensystem only  

        # TEILGELIEFERT
        VERSANDT_AN_K                       = '10', ('Geliefert|' + KUNDENDIENST + '|90%')
        # GELIEFERT - MINSTATUS GELIEFERT (aka alle geliefert)
        GELIEFERT                           = '11', ('Geliefert|' + KUNDEN + '|90%') # für Kundensystem only 

        # ABGENOMMEN
        ABGENOMMEN                          = '13', ('Abgenommen||100%') # auch für Kundensystem #KD

        # STORNIERT
        STORNIERT                           = '14', ('Storniert||100%')

    status = models.CharField(
        max_length = 2,
        choices = Status.choices,
        default = Status.ERFASST,
    )

    cust_order = models.ForeignKey(CustOrder, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    
    def get_status_display(self):
        return self.Status(self.status).label.split("|", 2)[0]

    def get_status_progress(self):
        return self.Status(self.status).label.split("|", 2)[-1]
    
    def group_has_work(self, user):
        for group in Group.objects.filter(name__in=self.Status(self.status).label.split("|", 2)[1].split(',')):
            if user.groups.filter(name=group).exists():
                return True
        return False

    def get_min_status(self):
        # here to avoid import loop
        minstatus = 9000
        for i in CustOrderDet.objects.filter(cust_order=self.cust_order.pk):
            if int(i.status) < minstatus:
                minstatus = int(i.status)
        return minstatus

    def save(self, *args, **kwargs):
        super(CustOrderDet, self).save(*args, **kwargs)
        self.postsave()

    def postsave(self):
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
                if CustOrderDet.objects.filter(cust_order=self.cust_order, status=self.Status.GELIEFERT).exists():
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
                if CustOrderDet.objects.filter(cust_order=self.cust_order, status=self.Status.GELIEFERT).exists():
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