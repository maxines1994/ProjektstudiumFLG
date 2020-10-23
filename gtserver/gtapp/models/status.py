from django.db import models

class Status(models.Model):
    """
    This model contains information about the meaning of all statuses for all tables.
    """ 

    table = models.CharField(max_length=30)
    status = models.CharField(max_length=1)
    description_en = models.CharField(max_length=30)
    description_de = models.CharField(max_length=30)