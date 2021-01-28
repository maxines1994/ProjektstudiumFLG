from django.db import models
from django.contrib.auth.models import User
from . import GtModel

class Complaint(GtModel):
    """
    Das ist eine Abstrakte Klasse und dient als Vorlage fuer Kopfdaten der Lieferanten-Reklamationen und Kunden-Reklamationen
    """

    class Status(models.TextChoices):

        DEFAULT                = '0', ('Standard')
        BEING_CREATED          = '1', ('Wird erstellt')
        RECEIVED               = '2', ('Empfangen')
        DONE                   = '3', ('Erledigt')

    finished_on = models.SmallIntegerField(null=True, blank=True)
    memo = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    box_no = models.CharField(max_length=8,null=True,blank=True)
   
    status = models.CharField(
        max_length = 1,
        choices = Status.choices,
        default = Status.DEFAULT,
    )

    class Meta:
        abstract = True
