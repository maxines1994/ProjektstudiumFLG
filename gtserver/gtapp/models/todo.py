from django.db import models
from django.contrib.auth.models import User
from gtapp.constants.general import *
from . import GtModel, CustOrderDet, TodoType
import time

class Todo(GtModel):
    """
    Dieses Model enthaelt die einzelnen Todos. Es identifiziert den Todo-Typ und den Sachbearbeiter des Todos.
    Ausserdem enthaelt es die Zuordnung zur Bestellposition, sowie ein Notizfeld.
    """

    memo = models.TextField()
    finished_on = models.SmallIntegerField()
    todo_type = models.ForeignKey(TodoType, on_delete=models.CASCADE)
    cust_order_det = models.ForeignKey(CustOrderDet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=UNKNOWN, on_delete=models.SET_DEFAULT)