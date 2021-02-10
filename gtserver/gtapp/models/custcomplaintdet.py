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
        IN_ANPASSUNG                    = '4', ('In Anpassung')
        ANPASSUNG_ABGESCHLOSSEN         = '5', ('Anpassung abgeschlossen')
        BEI_KUNDENDIENST       = '6', ('Bei Kundendienst')
        GELIEFERT                       = '7', ('Geliefert')

    status = models.CharField(
        max_length = 1,
        choices = Status.choices,
        default = Status.ERFASST,
    )
    
    cust_complaint = models.ForeignKey(CustComplaint, on_delete=models.CASCADE)
    cust_order_det = models.ForeignKey(CustOrderDet, on_delete=models.CASCADE)
