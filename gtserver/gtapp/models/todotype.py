from django.db import models
from gtapp.constants import *
from django.contrib.auth.models import Group
from . import GtModel

class TodoType(GtModel):
    """
    Dieses Model enthaelt die einzelnen Arten von Todos und Ihre Zuordnung zur Nutzergruppe, die diese Todoart bekommt.
    Es enthaelt ein Kuerzel, sowie eine Beschreibung auf Deutsch und Englisch.
    """

    type = models.CharField(max_length=3)
    description_en = models.CharField(max_length=150)
    description_de = models.CharField(max_length=150)    
    group = models.ForeignKey(Group,null=True, on_delete=models.SET_NULL)
    title_de = models.CharField(max_length=50)
    title_en = models.CharField(max_length=50)