from django.db import models
from . import Container, CustOrderDet

class CustContainer(Container):
    """
    Dieses Model enthalt Informationen ueber Container, in denen die fertigen Hubbuehnen zum Kunden transportiert werden.
    Container werden mittels Barcode zu den Auftragspositionen verknuepft.
    """    

    cust_order_det = models.ForeignKey(CustOrderDet, on_delete=models.CASCADE)