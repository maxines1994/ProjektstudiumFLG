from django.db import models
from . import Status, Part
from gtapp.constants import *


class Article(models.Model):
    """
    This model contains master data of the lifting platforms that are sold to the costumers.
    """

    status = models.ForeignKey(Status,null=True, on_delete=models.SET_NULL)
    article_no = models.CharField(max_length=8)
    description = models.CharField(max_length=30)
    parts = models.ManyToManyField(Part, through='ArtiPart')