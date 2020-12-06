from django.db import models
from . import GtModelBasic

class BookingCode(GtModelBasic):
    """
    Dieses Model enthaelt die Lagerbuchungscodes mit der entsprechenden Beschreibung auf Deutsch und Englisch.
    """

    code = models.CharField(max_length=3)
    description_en = models.CharField(max_length=30)
    description_de = models.CharField(max_length=30)

    def __str__(self):
        return self.description_de