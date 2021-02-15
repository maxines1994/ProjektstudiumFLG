from django.db import models
from django.contrib.auth.models import User
from gtapp.constants.general import *
from gtapp.models import *
import time

class Task(GtModel):
    """
    Dieses Model enthaelt die einzelnen Tasks. Es identifiziert den Task-Typ und den Sachbearbeiter des Tasks.
    Ausserdem enthaelt es die Zuordnung zur Bestellposition, sowie ein Notizfeld.
    """
    
    class Status(models.TextChoices):

        NICHT_ZUGEWIESEN           = 1, ('Nicht zugewiesen')
        ZUGEWIESEN                 = 2, ('Zugewiesen')
        IN_BEARBEITUNG             = 3, ('In Bearbeitung')
        ERLEDIGT                   = 4, ('Erledigt')

    
    start_on = models.SmallIntegerField(null=True, blank=True)
    finished_on = models.SmallIntegerField(null=True, blank=True)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    cust_order = models.ForeignKey(CustOrder, null= True, on_delete=models.SET_NULL)
    cust_order_det = models.ForeignKey(CustOrderDet, null= True, on_delete=models.SET_NULL)
    supp_order = models.ForeignKey(SuppOrder, null= True, on_delete=models.SET_NULL)
    supp_order_det = models.ForeignKey(SuppOrderDet, null= True, on_delete=models.SET_NULL)
    cust_complaint = models.ForeignKey(CustComplaint, null= True, on_delete=models.SET_NULL)
    cust_complaint_det = models.ForeignKey(CustComplaintDet, null= True, on_delete=models.SET_NULL)
    supp_complaint = models.ForeignKey(SuppComplaint, null= True, on_delete=models.SET_NULL)
    supp_complaint_det = models.ForeignKey(SuppComplaintDet, null= True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    active = models.SmallIntegerField(null=True)

    status = models.CharField(
        max_length = 2,
        choices = Status.choices,
        default = Status.NICHT_ZUGEWIESEN,
    )
    
    @classmethod
    def set_task(cls, obj, task_type_id, day=Timers.get_current_day()):
        """
        Erstellt einen Task. Parameter sind das Objekt und die ID des Task-Typs
        """
        # Suche das Model des uebergebenen Objekts (CustOrder, CustOrderDet ...)
        my_model = GtModel.str_to_gtmodel(obj.__class__.__name__)
        # Wandle das Model in einen Fremdschluesselnamen nach hiesiger Konvention um
        # (cust_order, cust_order_det ...)
        my_fieldname = GtModel.gtmodel_to_foreign_field_name(my_model)
        # Baue Filter entsprechend des Feldnamens
        my_task_filter = {}
        # cust_order_id / cust_order_det_id /... = obj.id
        my_task_filter[my_fieldname + '_id'] = obj.id
        my_task_filter['task_type_id'] = task_type_id
        # Erweitere den Filter fuer die create-Methode
        my_create_filter = {}
        # Fuelle Fremdschluesselfeld z.B. cust_order_id, task_type_id, active=1 und start_on-Datum
        my_create_filter[my_fieldname + '_id'] = my_task_filter[my_fieldname + '_id']
        my_create_filter['task_type_id'] = my_task_filter['task_type_id']
        my_create_filter['active'] = 1
        my_create_filter['start_on'] = day

        if 'det' in my_fieldname:
            # Erweitere Filter zum Fuellen der ID des Kopf-models
            # Z.B bei CustOrderDets soll hier zur Erleichterung gleich 
            # die dazu gehoerende cust_order_id mitgespeichert werden.
            # Beispiel: cust_order_det wird in my_header_fieldname zu cust_order
            my_header_fieldname = my_fieldname.replace('_det', '')
            # Speichere bspw die cust_order_id von dieser CustOrderDet
            my_header_id = getattr(obj, my_header_fieldname)
            # gettattr(my_model, my_header_fieldname) entspricht fuer my_model = CustOrderDet:
            # obj.cust_order. Es wird also die CustOrder des Objekts des Typs CustOrderDet ermittelt.
            my_create_header_filter = {}
            my_create_header_filter[my_fieldname + '_id'] = my_create_filter[my_fieldname + '_id']
            my_create_header_filter['task_type_id'] = my_create_filter['task_type_id']
            my_create_header_filter['active'] = my_create_filter['active']
            my_create_header_filter['start_on'] = my_create_filter['start_on']
            my_create_header_filter[my_header_fieldname] = getattr(obj, my_header_fieldname)
            # Fueg das Feld zum create-Filter hinzu, damit z.B. die cust_order_id mitgespeichert wird.
            my_create_filter[my_header_fieldname] = my_header_id

        if not Task.objects.filter(**my_task_filter):
            # Nur erzeugen, wenn es den Task noch nicht gibt.
            Task.objects.create(**my_create_filter)

    @classmethod
    def get_tasks_of_user(self, user):
        return Task.objects.filter(user=user, active=1)

    @classmethod
    def get_unassigned_tasks(self, user):
        return Task.objects.filter(user=None, active=1, task_type__group__in=user.groups.all())

    @classmethod
    def has_unassigned(self, user):
        return Task.get_unassigned_tasks(user).exists()

    def get_ref(self):
        out = '-'

        # CustOrder mit Position
        if self.cust_order:
            out = self.cust_order.__str__()
            if self.cust_order_det:
                out += '-' + self.cust_order_det.__str__()

        # CustComplaint mit Position
        elif self.cust_complaint:
            out = self.cust_complaint.__str__()
            if self.cust_complaint_det:
                out += '-' + self.cust_complaint_det.__str__()

        # SuppOrder mit Position
        elif self.supp_order:
            out = self.supp_order.__str__()
            if self.supp_order_det:
                out += '-' + self.supp_order_det.__str__()

        # SuppComplaint mit Position
        elif self.supp_complaint:
            out = self.supp_complaint.__str__()
            if self.supp_complaint_det:
                out += '-' + self.supp_complaint_det.__str__()

        return out

    def __str__(self):
        return self.task_type.title + ' (' + self.get_ref() + ')'
