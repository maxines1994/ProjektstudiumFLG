from django.db import models
from . import GtModel

class Customer(GtModel):
    """
    Dieses Model enthaelt die Stammdaten der Kunden.
    """ 

    name = models.CharField(max_length=30)
    memo = models.TextField(null=True)

    def __str__(self):
        return self.name