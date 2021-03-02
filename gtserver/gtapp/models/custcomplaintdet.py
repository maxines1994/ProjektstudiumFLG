from django.db import models
from . import ComplaintDet, CustComplaint, CustOrderDet
from gtapp.constants import *
from django.contrib.auth.models import Group

class CustComplaintDet(ComplaintDet):
    """
    Dieses Model enthaelt die Positionen von Kundenreklamationen
    """

    class Status(models.TextChoices):

        ERFASST                         = '0', ('Erfasst|'+ KUNDENDIENST +','+ KUNDEN +'|0%')
        REKLAMATION_FREIGEGEBEN         = '1', ('Reklamation freigegeben|'+ KUNDENDIENST +','+ KUNDEN +'|10%')
        IN_REKLAMATION                  = '2', ('In Reklamation|'+ KUNDEN +'|50%') ##Nur für den Kunden
        VERSAND_AN_PRODUKTION           = '3', ('Versandt an Produktion|'+ PRODUKTION +'|20%')
        IN_ANPASSUNG                    = '4', ('In Anpassung|'+ PRODUKTION +'|30%')
        ANPASSUNG_ABGESCHLOSSEN         = '5', ('Anpassung abgeschlossen|'+ PRODUKTION +'|50%')
        VERSAND_AN_KUNDENDIENST         = '6', ('Versandt an Kundendienst|'+ KUNDENDIENST +'|60%')
        BEI_KUNDENDIENST                = '7', ('Bereit zum Versand an Kunden|'+ KUNDENDIENST +'|70%')
        VERSAND_AN_KUNDE                = '8', ('Versandt an Kunde|'+ KUNDENDIENST+'|80%')
        GELIEFERT                       = '9', ('Geliefert||90%')
        ABGESCHLOSSEN                   = '10', ('Abgeschlossen||100%')

    status = models.CharField(
        max_length = 2,
        choices = Status.choices,
        default = Status.ERFASST,
    )
    
    cust_complaint = models.ForeignKey(CustComplaint, on_delete=models.CASCADE)
    cust_order_det = models.ForeignKey(CustOrderDet, on_delete=models.CASCADE)
    
    def get_status_display(self):
        return self.Status(self.status).label.split("|", 2)[0]

    def get_status_progress(self):
        return self.Status(self.status).label.split("|", 2)[-1]
    
    def group_has_work(self, user):
        for group in Group.objects.filter(name__in=self.Status(self.status).label.split("|", 2)[1].split(',')):
            if user.groups.filter(name=group).exists():
                return True
        return False


    def __str__(self):
        return self.pos.__str__()

    def get_min_status(self):
        # here to avoid import loop
        minstatus = 9000
        for i in CustComplaintDet.objects.filter(cust_complaint=self.cust_complaint.pk):
            if int(i.status) < minstatus:
                minstatus = int(i.status)
        return minstatus

    def save(self, *args, **kwargs):
        super(CustComplaintDet, self).save(*args, **kwargs)
        self.postsave()

    def postsave(self):
        # Status auf Kopfebene setzen
        # Normale Status
        minstatus = self.get_min_status()

        if self.cust_complaint.external_system == False:
            # JOGA
            if minstatus <= int(self.Status.ERFASST):
                self.cust_complaint.status = CustComplaint.Status.ERFASST
            elif minstatus <= int(self.Status.REKLAMATION_FREIGEGEBEN):
                self.cust_complaint.status = CustComplaint.Status.REKLAMATION_FREIGEGEBEN
            elif minstatus <= int(self.Status.VERSAND_AN_PRODUKTION):
                self.cust_complaint.status = CustComplaint.Status.VERSAND_AN_PRODUKTION
            elif minstatus <= int(self.Status.IN_ANPASSUNG):
                self.cust_complaint.status = CustComplaint.Status.IN_ANPASSUNG
            elif minstatus <= int(self.Status.VERSAND_AN_KUNDENDIENST):
                self.cust_complaint.status = CustComplaint.Status.VERSAND_AN_KUNDENDIENST
            elif minstatus <= int(self.Status.BEI_KUNDENDIENST):
                self.cust_complaint.status = CustComplaint.Status.BEI_KUNDENDIENST
            elif minstatus <= int(self.Status.VERSAND_AN_KUNDE):
                self.cust_complaint.status = CustComplaint.Status.VERSAND_AN_KUNDE
            elif minstatus <= int(self.Status.ABGESCHLOSSEN):
                self.cust_complaint.status = CustComplaint.Status.ABGESCHLOSSEN

        else:
            # Kundensystem
            if minstatus <= int(self.Status.ERFASST):
                self.cust_complaint.status = CustComplaint.Status.ERFASST
            elif minstatus <= int(self.Status.REKLAMATION_FREIGEGEBEN):
                self.cust_complaint.status = CustComplaint.Status.REKLAMATION_FREIGEGEBEN
            elif minstatus <= int(self.Status.IN_REKLAMATION):
                self.cust_complaint.status = CustComplaint.Status.IN_REKLAMATION
            elif minstatus <= int(self.Status.ABGESCHLOSSEN):
                self.cust_complaint.status = CustComplaint.Status.ABGESCHLOSSEN

        self.cust_complaint.save()
