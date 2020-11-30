from django.db import models
from django.apps import apps
from . import OrderDet, CustOrder, Article

class CustOrderDet(OrderDet):
    """
    This model contains detailed information for every position of a Costumer-Order.
    It inherits most of its fields from the abstract OrderDet-Class.
    """   

    cust_order = models.ForeignKey(CustOrder, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)