from django.db import models
from . import GtModel

class OrderDet(GtModel):
    """
    Das ist eine Abstrakte Klasse und dient als Vorlage fuer Positionsdaten der Bestellungen und Auftraege.
    """
    
    pos = models.IntegerField()
    unit_price = models.IntegerField()
    received_on = models.SmallIntegerField()
    memo = models.TextField()

    class Meta:
        abstract = True