from django.db import models
from . import Status, Part
"""
This model contains master data of the lifting platforms that are sold to the costumers.
"""

class Article(models.Model):
    Status = models.ForeignKey(Status, on_delete=models.CASCADE)
    ArticleNo = models.CharField(max_length=8)
    Description = models.CharField(max_length=30)
    Parts = models.ManyToManyField(Part, through='ArtiPart')