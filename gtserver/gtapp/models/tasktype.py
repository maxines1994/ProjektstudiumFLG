from django.db import models
from gtapp.constants import *
from django.contrib.auth.models import Group
from . import GtModel

class TaskType(GtModel):
    """
    Dieses Model enthaelt die einzelnen Arten von Tasks und Ihre Zuordnung zur Nutzergruppe, die diese Taskart bekommt.
    Es enthaelt ein Kuerzel, sowie eine Beschreibung auf Deutsch und Englisch.
    """

    code = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=150)    
    title = models.CharField(max_length=50)
    status_model = models.CharField(max_length=50)
    task_model = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    view_url = models.CharField(max_length=50)
    view_kwargs_id = models.CharField(max_length=50)
    for_all_details = models.BooleanField(default=False)
    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)