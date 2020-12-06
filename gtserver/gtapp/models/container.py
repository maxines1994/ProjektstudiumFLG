from django.db import models
from . import GtModel

class Container(GtModel):
    """
    Das ist eine Abstrakte Klasse und dient als Vorlage fuer Lieferanten-Container und Kunden-Container.
    """   

    barcode = models.CharField(max_length=8)
    delivery_date = models.SmallIntegerField()
    memo = models.TextField()

    class Meta:
        abstract = True