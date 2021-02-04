from django.db import models
from . import ComplaintDet, CustComplaint, CustOrderDet

class CustComplaintDet(ComplaintDet):
    """
    Dieses Model enthaelt die Positionen von Kundenreklamationen
    """

    class Status(models.TextChoices):

        STANDARD                        = '0', ('Standard')
        ERFASST                         = '1', ('Erfasst')
        REKLAMATION_FREIGEGEBEN         = '2', ('Reklamation freigegeben')
        IN_REPARATUR                    = '3', ('In Reparatur')
        LIEFERUNG_AN_KUNDENDIENST       = '4', ('Lieferung an Kundendienst')
        LIEFERUNG_AN_KUNDE              = '5', ('Lieferung an Kunde')
        GELIEFERT                       = '6', ('Geliefert')

    status = models.CharField(
        max_length = 1,
        choices = Status.choices,
        default = Status.STANDARD,
    )
    
    cust_complaint = models.ForeignKey(CustComplaint, on_delete=models.CASCADE)
    cust_order_det = models.ForeignKey(CustOrderDet, on_delete=models.CASCADE)
