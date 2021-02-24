from django.db import models
from . import ComplaintDet, SuppComplaint, SuppOrderDet, Timers, SuppOrder, Part
from gtapp.constants import *
from django.contrib.auth.models import Group

class SuppComplaintDet(ComplaintDet):
    """
    Diese Model enthaelt die Positionsdaten je Lieferanten-Reklamation.
    """
    supp_complaint = models.ForeignKey(SuppComplaint, on_delete=models.CASCADE)
    supp_order_det = models.ForeignKey(SuppOrderDet, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    redelivery = models.BooleanField(default=False)

    class Status(models.TextChoices):       
        ERFASST                         = '0', ('Erfasst||0%')
        VERSAND_AN_PDL                  = '1', ('Versandt an PDL||10%')
        IN_BEARBEITUNG                  = '2', ('In Bearbeitung||20%')
        REKLAMATION_FREIGEGEBEN         = '3', ('Reklamation freigegeben||30%')
        BESTANDSPRUEFUNG_ABGESCHLOSSEN  = '4', ('Bestandsprüfung abgeschlossen||33%')##Nur LF
        VERSAND_AN_KUNDE                = '5', ('Versandt an Kunde||67%')##Nur LF
        AUS_LAGER_GELIEFERT             = '6', ('Aus Lager beliefert||40%')
        NEU_BESTELLEN                   = '7', ('Teil neu bestellen||50%')
        VERSAND_AN_LIEFERANT            = '8', ('Versandt an Lieferant||70%')
        GELIEFERT                       = '9', ('Geliefert||80%')
        VERSAND_AN_PRODUKTION           = '10', ('Versandt an Produktion||90%')
        ABGESCHLOSSEN                   = '11', ('Abgeschlossen||100%')   

    status = models.CharField(
        max_length = 2,
        choices = Status.choices,
        default = Status.ERFASST,
    )
    
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
        return self.pos.__str__() + ' ' + self.supp_order_det.part.description

    def auto_complaint(supp_order_det_id_list:list, quantity_list:list):
        """
        Erwartet Listen von Teilen und Mengen und erzeugt daraus eine neue Reklamation
        mit entsprechenden Positionen. Gibt die ID der erstellten Reklamation zurueck
        """
        my_supp_order_id = SuppOrder.objects.get(id=SuppOrderDet.objects.get(id=supp_order_det_id_list[0]).supp_order_id).id
        new_suppcomplaint = SuppComplaint.objects.create(supp_order_id=my_supp_order_id, supplier_id=3, issued_on=Timers.get_current_day(), memo="Automatisch generiert")
        # Packe die Listen zusammen und iteriere ueber beide Listen
        supporderdet_quantity = zip(supp_order_det_id_list, quantity_list)
        i = 0
        for supp_order_det_id, quantity in supporderdet_quantity:
            my_part = Part.objects.get(id=SuppOrderDet.objects.get(id=supp_order_det_id).part_id)
            SuppComplaintDet.objects.create(supp_order_det_id=supp_order_det_id, supp_complaint=new_suppcomplaint, pos=i+1, quantity=quantity)
            i += 1

        return new_suppcomplaint.id
    
    def get_min_status(self):
        # here to avoid import loop
        minstatus = 9000
        for i in SuppComplaintDet.objects.filter(supp_complaint=self.supp_complaint.pk):
            if int(i.status) < minstatus:
                minstatus = int(i.status)
        return minstatus

    def save(self, *args, **kwargs):

        # Status auf Kopfebene setzen
        # Normale Status
        minstatus = self.get_min_status()

        if self.supp_complaint.external_system == False:
            # JOGA
            if minstatus <= int(self.Status.ERFASST):
                self.supp_complaint.status = SuppComplaint.Status.ERFASST
            elif minstatus <= int(self.Status.VERSAND_AN_PDL):
                self.supp_complaint.status = SuppComplaint.Status.VERSAND_AN_PDL
            elif minstatus <= int(self.Status.IN_BEARBEITUNG):
                self.supp_complaint.status = SuppComplaint.Status.IN_BEARBEITUNG
            elif minstatus <= int(self.Status.REKLAMATION_FREIGEGEBEN):
                self.supp_complaint.status = SuppComplaint.Status.REKLAMATION_FREIGEGEBEN
            elif minstatus <= int(self.Status.NEU_BESTELLEN):
                ## Prüfen ob die Positionen weiter prozessiert wurden
                pos_work_finished = True
                for i in SuppComplaintDet.objects.filter(supp_complaint=self.supp_complaint.pk):
                    if i.status in ['0','1','2','3','4','5','8','9','10']:
                        pos_work_finished = False
                if pos_work_finished:
                    self.supp_complaint.status = SuppComplaint.Status.POSITIONSBEARBEITUNG_FERTIG

        else:
            # Kundensystem
            if minstatus <= int(self.Status.ERFASST):
                self.supp_complaint.status = SuppComplaint.Status.ERFASST
            else:
                # Fallback
                self.supp_complaint.status = SuppComplaint.Status.ERFASST

        self.supp_complaint.save()
        super(SuppComplaintDet, self).save(*args, **kwargs)
