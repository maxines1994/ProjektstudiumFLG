from django.db import models
from . import GtModel

class BookingCode(GtModel):
    """
    Dieses Model enthaelt die Lagerbuchungscodes mit der entsprechenden Beschreibung auf Deutsch und Englisch.
    """

    code = models.CharField(max_length=3)
    description = models.CharField(max_length=30)

    def __str__(self):
        return self.description