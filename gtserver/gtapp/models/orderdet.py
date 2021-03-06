from django.db import models
from . import GtModel

class OrderDet(GtModel):
    """
    Das ist eine Abstrakte Klasse und dient als Vorlage fuer Positionsdaten der Bestellungen und Auftraege.
    """
    
    pos = models.IntegerField(blank=True)
    received_on = models.SmallIntegerField(blank=True, null=True)
    memo = models.TextField(blank=True, null=True)
    box_no = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        abstract = True