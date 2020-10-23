from django.db import models
from . import Status, Article, Part

class ArtiPart(models.Model):
    """
    This model maps the lifting platforms to each of its components with the respective component-quantity
    """

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()