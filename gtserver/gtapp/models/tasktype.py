from django.db import models
from gtapp.constants import *
from django.contrib.auth.models import Group
from . import GtModel

class TaskType(GtModel):
    """
    Dieses Model enthaelt die einzelnen Arten von Tasks und Ihre Zuordnung zur Nutzergruppe, die diese Taskart bekommt.
    Es enthaelt ein Kuerzel, sowie eine Beschreibung auf Deutsch und Englisch.
    """

    type = models.CharField(max_length=3)
    description = models.CharField(max_length=150)    
    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=50)