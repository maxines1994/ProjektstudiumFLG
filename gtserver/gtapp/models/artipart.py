from django.db import models
from . import GtModelBasic, Status, Article, Part

class ArtiPart(GtModelBasic):
    """
    Dieses Model ordnet die Artikel den Teilen mit der entsprechenden Menge zu, aus denen er besteht. 
    """

    quantity = models.SmallIntegerField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)