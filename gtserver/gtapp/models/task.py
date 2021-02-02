from django.db import models
from django.contrib.auth.models import User
from gtapp.constants.general import *
from . import GtModel, CustOrderDet, CustOrder, TaskType, GtModel, SuppOrder, SuppOrderDet
import time

class Task(GtModel):
    """
    Dieses Model enthaelt die einzelnen Tasks. Es identifiziert den Task-Typ und den Sachbearbeiter des Tasks.
    Ausserdem enthaelt es die Zuordnung zur Bestellposition, sowie ein Notizfeld.
    """
    
    class Status(models.TextChoices):

        DEFAULT                = '0', ('Standard')
        UNASSIGNED             = '1', ('Nicht zugewiesen')
        ASSIGNED               = '2', ('Zugewiesen')
        IN_PRORESS             = '3', ('In Bearbeitung')
        DONE                   = '4', ('Erledigt')

    
    start_on = models.SmallIntegerField(null=True, blank=True)
    finished_on = models.SmallIntegerField(null=True, blank=True)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    cust_order = models.ForeignKey(CustOrder, null= True, on_delete=models.SET_NULL)
    cust_order_det = models.ForeignKey(CustOrderDet, null= True, on_delete=models.SET_NULL)
    supp_order = models.ForeignKey(SuppOrder, null= True, on_delete=models.SET_NULL)
    supp_order_det = models.ForeignKey(SuppOrderDet, null= True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    active = models.SmallIntegerField(null=True)

    status = models.CharField(
        max_length = 1,
        choices = Status.choices,
        default = Status.DEFAULT,
    )
    

    #Task für CusOrders
    @classmethod
    def set_task_cust(cls, order, number, day):
        mylist = list(Task.objects.filter(cust_order_id = order, task_type_id=number))
        if not mylist:
                Task.objects.create(cust_order=order, task_type_id=number, active=1, start_on=day)
        else:
            pass 

    #Task für CusOrderDets
    @classmethod
    def set_task_cust_det(cls, orderdet, number, day):
        mylist = list(Task.objects.filter(cust_order_det_id = orderdet, task_type_id=number))
        if not mylist:
                Task.objects.create(cust_order_det=orderdet, task_type_id=number, active=1, start_on=day)
        else:
            pass

    #Task für SuppOrders
    @classmethod
    def set_task_supp(cls, order, number, day):
        mylist = list(Task.objects.filter(supp_order_id = order, task_type_id=number))
        if not mylist:
                Task.objects.create(supp_order=order, task_type_id=number, active = 1, start_on= day)
        else:
            pass  
    
    #Task für SuppOrderDets
    @classmethod
    def set_task_supp_det(cls, orderdet, number, day):
        mylist = list(Task.objects.filter(supp_order_det_id = orderdet, task_type_id=number))
        if not mylist:
                Task.objects.create(supp_order_det=orderdet, task_type_id=number, active = 1, start_on= day)
        else:
            pass
            pass 
    
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
        if self.cust_order_det:
            return self.cust_order_det.__str__()
        elif self.cust_order:
            return self.cust_order.__str__()
        return '-'

    def __str__(self):
        return self.task_type.title + ' (' + self.get_ref() + ')'
