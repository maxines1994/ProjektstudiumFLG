from django.db import models
from django.contrib.auth.models import Group
from . import GtModelBasic

class OrgaUnit(GtModelBasic):
    """
    Dieses Model erweitert die User-Tabelle um zusaetzliche Felder
    """

    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    code = models.CharField(max_length=3)
    name_de = models.CharField(max_length=30)