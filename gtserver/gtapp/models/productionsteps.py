from django.db import models
from . import GtModel
from .part import Part 
from .article import Article

class ProductionSteps(GtModel):
    """
    Das ist eine Klasse und dient als Vorlage fuer Datenbanktabelle fuer die Ausgabe der Teileliste
    """

    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    production_step = models.SmallIntegerField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
