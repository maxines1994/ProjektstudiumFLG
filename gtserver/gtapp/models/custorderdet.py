from django.db import models
from django.apps import apps
from . import OrderDet, CustOrder, Article

class CustOrderDet(OrderDet):
    """
    Dieses Model enthaelt die Positionsdaten eines Kundenauftrages.
    """   

    cust_order = models.ForeignKey(CustOrder, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return str(str(self.cust_order) + ": Artikel: "+ str(self.article) )
