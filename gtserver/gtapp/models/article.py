from django.db import models
from . import Part
"""
This model contains master data of the lifting platforms that are sold to the costumers.
"""

class Article(models.Model):
    Status = models.CharField(max_length=1)
    ArticleNo = models.CharField(max_length=8)
    Description = models.CharField(max_length=30)
    Parts = models.ManyToManyField(Part, through='ArtiPart')