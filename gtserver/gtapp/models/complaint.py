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
    order_no = models.CharField(max_length=8)
    external_system = models.BooleanField(default=False)
    ref_no = models.CharField(null=True, blank=True, max_length=10)
   
    status = models.CharField(
        max_length = 2,
        choices = Status.choices,
        default = Status.ERFASST,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.order_no

