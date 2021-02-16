from django.db import models
from . import ComplaintDet, CustComplaint, CustOrderDet

class CustComplaintDet(ComplaintDet):
    """
    Dieses Model enthaelt die Positionen von Kundenreklamationen
    """

    class Status(models.TextChoices):

        ERFASST                         = '0', ('Erfasst|0%')
        REKLAMATION_FREIGEGEBEN         = '1', ('Reklamation freigegeben|10%')
        IN_REKLAMATION                  = '2', ('In Reklamation|50%') ##Nur für den Kunden
        VERSAND_AN_PRODUKTION           = '3', ('Versand an Produktion|20%')
        IN_ANPASSUNG                    = '4', ('In Anpassung|30%')
        ANPASSUNG_ABGESCHLOSSEN         = '5', ('Anpassung abgeschlossen|50%')
        VERSAND_AN_KUNDENDIENST         = '6', ('Versand an Kundendienst|60%')
        BEI_KUNDENDIENST                = '7', ('Bei Kundendienst|70%')
        VERSAND_AN_KUNDE                = '8', ('Versand an Kunde|80%')
        GELIEFERT                       = '9', ('Geliefert|90%')
        ABGESCHLOSSEN                   = '10', ('Abgeschlossen|100%')

    status = models.CharField(
        max_length = 2,
        choices = Status.choices,
        default = Status.ERFASST,
    )

    def get_status_display(self):
        return self.Status(self.status).label.split("|", 1)[0]

    def get_status_progress(self):
        return self.Status(self.status).label.split("|", 1)[-1]
    
    cust_complaint = models.ForeignKey(CustComplaint, on_delete=models.CASCADE)
    cust_order_det = models.ForeignKey(CustOrderDet, on_delete=models.CASCADE)

    def __str__(self):
        return self.pos.__str__()
