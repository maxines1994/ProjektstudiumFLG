from django.db import models
from gtapp.constants import *
from django.contrib.auth.models import Group
from . import GtModelBasic

class TodoType(GtModelBasic):
    """
    Dieses Model enthaelt die einzelnen Arten von Todos und Ihre Zuordnung zur Nutzergruppe, die diese Todoart bekommt.
    Es enthaelt ein Kuerzel, sowie eine Beschreibung auf Deutsch und Englisch.
    """

    type = models.CharField(max_length=3)
    description_en = models.CharField(max_length=30)
    description_de = models.CharField(max_length=30)    
    parent = models.ForeignKey('self', null=True, related_name='parent_todo', on_delete=models.SET_NULL)
    child = models.ForeignKey('self', null=True, related_name='child_todo', on_delete=models.SET_NULL)
    group = models.ForeignKey(Group,null=True, on_delete=models.SET_NULL)