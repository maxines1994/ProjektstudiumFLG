from django.db import models
from . import Container, SuppOrderDet

class SuppContainer(Container):
    """
    Dieses Model enthalt Informationen ueber Container, in denen die Teile vom Lieferanten zu JOGA transportiert werden.
    Container werden mittels Barcode zu den Bestellpositionen verknuepft.
    """  

    supp_order_det = models.ForeignKey(SuppOrderDet, on_delete=models.CASCADE)