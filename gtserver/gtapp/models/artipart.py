from django.db import models
from . import GtModel, Article, Part

class ArtiPart(GtModel):
    """
    Dieses Model ordnet die Artikel den Teilen mit der entsprechenden Menge zu, aus denen er besteht. 
    """

    quantity = models.SmallIntegerField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.part.description)