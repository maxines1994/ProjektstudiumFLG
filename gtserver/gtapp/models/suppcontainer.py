from django.db import models
from . import SuppOrderDet

"""
This is model contains the information about Containers that are used to ship parts from
the supplier. They are used to map the container via Barcode to the Supplier-Order-Details.
It inherits most of its fields from the abstract Container-Class
"""

class SuppContainer(models.Model):
    SuppOrderDet = models.ForeignKey(SuppOrderDet, on_delete=models.CASCADE)