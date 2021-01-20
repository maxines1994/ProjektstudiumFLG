from django.db import models
from django.contrib.auth.models import User
from . import GtModel

class Complaint(GtModel):
    """
    Das ist eine Abstrakte Klasse und dient als Vorlage fuer Kopfdaten der Lieferanten-Reklamationen und Kunden-Reklamationen
    """

    finished_on = models.SmallIntegerField(null=True, blank=True)
    memo = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True
