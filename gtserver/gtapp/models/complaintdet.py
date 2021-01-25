from django.db import models
from . import GtModel

class ComplaintDet(GtModel):
    """
    Das ist eine Abstrakte Klasse und dient als Vorlage fuer die Einzelpositionen von Lieferanten-Reklamationen und Kunden-Reklamationen.
    """

    pos = models.SmallIntegerField()
    memo = models.TextField()

    class Meta:
        abstract = True