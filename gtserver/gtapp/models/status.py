from django.db import models

"""
This model contains information about the meaning of all states for all tables.
This table ist just for internal documentation and not meant to be mapped to other models.
"""

class Status(models.Model):
    Table = models.CharField(max_length=30)
    Status = models.CharField(max_length=1)
    Description = models.CharField(max_length=30)