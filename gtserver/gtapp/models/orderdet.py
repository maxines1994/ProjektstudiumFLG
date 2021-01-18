from django.db import models
from . import GtModel

class OrderDet(GtModel):
    """
    Das ist eine Abstrakte Klasse und dient als Vorlage fuer Positionsdaten der Bestellungen und Auftraege.
    """
    
    pos = models.IntegerField(blank=True)
    unit_price = models.IntegerField(blank=True, null=True)
    received_on = models.SmallIntegerField(blank=True, null=True)
    memo = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True