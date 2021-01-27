from django.db import models
from . import GtModel

class Status(GtModel):
    """
    Dieses Model enthaelt die Status je Tabelle und ihre Bedeutung auf Deutsch und Englisch.
    """ 

    table = models.CharField(max_length=30)
    code = models.CharField(max_length=1)
    description_en = models.CharField(max_length=30)
    description_de = models.CharField(max_length=30)

    def __str__(self):
        return self.description_de