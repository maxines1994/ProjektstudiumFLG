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

        STANDARD                        = '0', ('Standard')
        ERFASST                         = '1', ('Erfasst')
        BEI_PDL                         = '2', ('Bei PDL') ##Nur wenn Rekla in PRO erstellt
        AUS_LAGER_LIEFERN               = '3', ('Aus Lager geliefert')
        NEU_BESTELLEN                   = '4', ('Neu bestellen')
        BESTANDSPRUEFUNG_AUSSTEHEND     = '5', ('Bestandsprüfung ausstehend')
        GELIEFERT                       = '6', ('Geliefert')
        ABGESCHLOSSEN                   = '7', ('Abgeschlossen') ##Nur wenn keine Neulieferung

    status = models.CharField(
        max_length = 1,
        choices = Status.choices,
        default = Status.ERFASST,
    )

    def __str__(self):
        return str(self.supp_order_det.part.description)