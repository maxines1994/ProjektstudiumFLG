from django.db import models
from . import ComplaintDet, SuppComplaint, SuppOrderDet

class SuppComplaintDet(ComplaintDet):
    """
    Diese Model enthaelt die Positionsdaten je Lieferanten-Reklamation.
    """
    supp_complaint = models.ForeignKey(SuppComplaint, on_delete=models.CASCADE)
    supp_order_det = models.ForeignKey(SuppOrderDet, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    redelivery = models.BooleanField(default=False)

    class Status(models.TextChoices):

        ERFASST                         = '0', ('Erfasst')
        VERSAND_AN_PDL                  = '1', ('Versand an PDL')
        IN_BEARBEITUNG                  = '2', ('In Bearbeitung')
        REKLAMATION_FREIGEGEBEN         = '3', ('Reklamation freigegeben')
        BESTANDSPRUEFUNG_ABGESCHLOSSEN  = '4', ('Bestandsprüfung abgeschlossen')##Nur LF
        VERSAND_AN_KUNDE                = '5', ('Versand an Kunde')##Nur LF
        AUS_LAGER_GELIEFERT             = '6', ('Aus Lager beliefert')
        NEU_BESTELLEN                   = '7', ('Teil neu bestellen')
        VERSAND_AN_LIEFERANT            = '8', ('Versand an Lieferant')
        GELIEFERT                       = '9', ('Geliefert')
        VERSAND_AN_PRODUKTION           = 'A', ('Versand an Produktion')
        ABGESCHLOSSEN                   = 'B', ('Abgeschlossen')   

    status = models.CharField(
        max_length = 1,
        choices = Status.choices,
        default = Status.ERFASST,
    )

    def __str__(self):
        return str(self.supp_order_det.part.description)