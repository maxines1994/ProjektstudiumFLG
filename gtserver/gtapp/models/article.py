from django.db import models
from . import GtModel, Part
from gtapp.constants import *


class Article(GtModel):
    """
    Dieses Model enthaelt die Stammdaten der Hubbuehnen, die an die Kunden verkauft werden.
    """

    article_no = models.CharField(max_length=8)
    description = models.CharField(max_length=30)
    parts = models.ManyToManyField(Part, through='ArtiPart')

    def __str__(self):
        return self.description