from django.db import models
from . import Article, Part

"""
This model maps the lifting platforms to each of its components with the respective component-quantity
"""

class ArtiPart(models.Model):
    Article = models.ForeignKey(Article, on_delete=models.CASCADE)
    Part = models.ForeignKey(Part, on_delete=models.CASCADE)
    Quantity = models.SmallIntegerField()