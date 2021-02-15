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
        ERFASST                         = '0', ('Erfasst|0%')
        VERSAND_AN_PDL                  = '1', ('Im Versand an PDL|10%')
        IN_BEARBEITUNG                  = '2', ('In Bearbeitung|20%')
        REKLAMATION_FREIGEGEBEN         = '3', ('Reklamation freigegeben|30%')
        BESTANDSPRUEFUNG_ABGESCHLOSSEN  = '4', ('Bestandsprüfung abgeschlossen|33%')##Nur LF
        VERSAND_AN_KUNDE                = '5', ('Im Versand an Kunde|67%')##Nur LF
        AUS_LAGER_GELIEFERT             = '6', ('Aus Lager beliefert|40%')
        NEU_BESTELLEN                   = '7', ('Teil neu bestellen|50%')
        VERSAND_AN_LIEFERANT            = '8', ('Im Versand an Lieferant|70%')
        GELIEFERT                       = '9', ('Geliefert|80%')
        VERSAND_AN_PRODUKTION           = '10', ('Im Versand an Produktion|90%')
        ABGESCHLOSSEN                   = '11', ('Abgeschlossen|100%')   

    status = models.CharField(
        max_length = 2,
        choices = Status.choices,
        default = Status.ERFASST,
    )
    
    def get_status_display(self):
        return self.Status(self.status).label.split("|", 1)[0]

    def get_status_progress(self):
        return self.Status(self.status).label.split("|", 1)[-1]

    def __str__(self):
        return self.pos.__str__() # supp_order_det.part.description)