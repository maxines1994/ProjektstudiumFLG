from django.db import models
from . import ComplaintDet, CustComplaint, CustOrderDet

class CustComplaintDet(ComplaintDet):
    """
    Dieses Model enthaelt die Positionen von Kundenreklamationen
    """

    class Status(models.TextChoices):

        STANDARD                        = '0', ('Standard')
        ERFASST                         = '1', ('Erfasst')
        IN_REKLAMATION                  = '2', ('In Reklamation') ##Nur für den Kunden
        REKLAMATION_FREIGEGEBEN         = '3', ('Reklamation freigegeben')
        IN_REPARATUR                    = '4', ('In Reparatur')
        REPARATUR_ABGESCHLOSSEN         = '5', ('Reparatur abgeschlossen')
        LIEFERUNG_AN_KUNDENDIENST       = '6', ('Lieferung an Kundendienst')
        LIEFERUNG_AN_KUNDE              = '7', ('Lieferung an Kunde')
        GELIEFERT                       = '8', ('Geliefert')

    status = models.CharField(
        max_length = 1,
        choices = Status.choices,
        default = Status.STANDARD,
    )
    
    cust_complaint = models.ForeignKey(CustComplaint, on_delete=models.CASCADE)
    cust_order_det = models.ForeignKey(CustOrderDet, on_delete=models.CASCADE)
