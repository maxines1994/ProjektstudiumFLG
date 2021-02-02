from django.db import models
from . import GtModel

class ComplaintDet(GtModel):
    """
    Das ist eine Abstrakte Klasse und dient als Vorlage fuer die Einzelpositionen von Lieferanten-Reklamationen und Kunden-Reklamationen.
    """
    class Status(models.TextChoices):

        DEFAULT                = '0', ('Standard')
        RECEIVED               = '1', ('Empfangen')
        DONE                   = '2', ('Erledigt')

    pos = models.SmallIntegerField()
    memo = models.TextField()
    box_no = models.CharField(max_length=8, null=True, blank=True)

    status = models.CharField(
        max_length = 1,
        choices = Status.choices,
        default = Status.DEFAULT,
    )

    class Meta:
        abstract = True