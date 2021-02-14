from django.db import models
from . import ComplaintDet, CustComplaint, CustOrderDet

class CustComplaintDet(ComplaintDet):
    """
    Dieses Model enthaelt die Positionen von Kundenreklamationen
    """

    class Status(models.TextChoices):

        ERFASST                         = '0', ('Erfasst')
        REKLAMATION_FREIGEGEBEN         = '1', ('Reklamation freigegeben')
        IN_REKLAMATION                  = '2', ('In Reklamation') ##Nur für den Kunden
        VERSAND_AN_PRODUKTION           = '3', ('Versand an Produktion')
        IN_ANPASSUNG                    = '4', ('In Anpassung')
        ANPASSUNG_ABGESCHLOSSEN         = '5', ('Anpassung abgeschlossen')
        VERSAND_AN_KUNDENDIENST         = '6', ('Versand an Kundendienst')
        BEI_KUNDENDIENST                = '7', ('Bei Kundendienst')
        VERSAND_AN_KUNDE                = '8', ('Versand an Kunde')
        GELIEFERT                       = '9', ('Geliefert')

    status = models.CharField(
        max_length = 1,
        choices = Status.choices,
        default = Status.ERFASST,
    )
    
    cust_complaint = models.ForeignKey(CustComplaint, on_delete=models.CASCADE)
    cust_order_det = models.ForeignKey(CustOrderDet, on_delete=models.CASCADE)
