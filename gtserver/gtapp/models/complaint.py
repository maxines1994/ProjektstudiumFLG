from django.db import models
from django.contrib.auth.models import User
from . import GtModel

class Complaint(GtModel):
    """
    Das ist eine Abstrakte Klasse und dient als Vorlage fuer Kopfdaten der Lieferanten-Reklamationen und Kunden-Reklamationen
    """

    class Status(models.TextChoices):

        ERFASST                 = 1, ('Erfasst')
        EMPFANGEN               = 2, ('Empfangen')
        ERLEDIGT                = 3, ('Erledigt')

    finished_on = models.SmallIntegerField(null=True, blank=True)
    memo = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    box_no = models.CharField(max_length=8, null=True, blank=True)
   
    status = models.CharField(
        max_length = 2,
        choices = Status.choices,
        default = Status.ERFASST,
    )

    class Meta:
        abstract = True
