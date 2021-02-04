from django.db import models
from .complaint import Complaint
from .custorder import CustOrder

class CustComplaint(Complaint):
    """
    Dieses Model enthaelt die Kopfdaten von Kundenreklamationen
    """

    class Status(models.TextChoices):

        STANDARD                        = '0', ('Standard')
        ERFASST                         = '1', ('Erfasst')
        IN_REKLAMATION                  = '2', ('In Reklamation') ##Nur für den Kunden
        REKLAMATION_FREIGEGEBEN         = '3', ('Reklamation freigegeben')
        IN_ANPASSUNG                    = '4', ('In Anpassung')
        ANPASSUNG_ABGESCHLOSSEN         = '5', ('Anpassung abgeschlossen')
        LIEFERUNG_AN_KUNDENDIENST       = '6', ('Lieferung an Kundendienst')
        LIEFERUNG_AN_KUNDE              = '7', ('Lieferung an Kunde')
        GELIEFERT                       = '8', ('Geliefert')

    status = models.CharField(
        max_length = 1,
        choices = Status.choices,
        default = Status.STANDARD,
    )

    cust_order = models.ForeignKey(CustOrder, on_delete=models.CASCADE)

