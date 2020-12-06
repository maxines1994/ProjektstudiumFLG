from django.db import models
from . import GtModel

class Supplier(GtModel):
    """
    Diese Model enthaelt die Stammdaten der Lieferanten, die die Einzelteile verkaufen, welche zum Bau der Hubbuehnen gebraucht werden.
    """

    name = models.CharField(max_length=30)
    memo = models.TextField()

    def __str__(self):
        return self.name