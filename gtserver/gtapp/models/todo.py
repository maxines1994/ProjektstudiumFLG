from django.db import models
from django.contrib.auth.models import User
from gtapp.constants.general import *
from . import GtModel, CustOrderDet, CustOrder, TodoType, GtModelBasic
import time

class Todo(GtModelBasic):
    """
    Dieses Model enthaelt die einzelnen Todos. Es identifiziert den Todo-Typ und den Sachbearbeiter des Todos.
    Ausserdem enthaelt es die Zuordnung zur Bestellposition, sowie ein Notizfeld.
    """

    
    start_on = models.SmallIntegerField(null=True)
    finished_on = models.SmallIntegerField(null=True)
    todo_type = models.ForeignKey(TodoType, on_delete=models.CASCADE)
    cust_order = models.ForeignKey(CustOrder, null= True, on_delete=models.SET_NULL)
    cust_order_det = models.ForeignKey(CustOrderDet, null= True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    active = models.SmallIntegerField(null=True)
    

    #erstes ToDo erstellen mit Auftragsnummer
    @classmethod
    def set_first_todo(cls, order, number, day):
        mylist = list(Todo.objects.filter(cust_order_id = order))
        if not mylist:
                Todo.objects.create(cust_order=order, todo_type_id=number, active = 1, start_on= day)
        else:
            pass 

    @classmethod
    def set_todo(cls, orderdet, number, day):
        mylist = list(Todo.objects.filter(cust_order_det_id = orderdet))
        if not mylist:
                Todo.objects.create(cust_order_det=orderdet, todo_type_id=number, active = 1, start_on= day)
        else:
            pass 