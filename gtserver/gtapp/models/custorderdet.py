from django.db import models
from django.apps import apps
from . import OrderDet, CustOrder, Article

"""
This model contains detailed information for every position of a Costumer-Order.
It inherits most of its fields from the abstract OrderDet-Class.
"""

class CustOrderDet(OrderDet):
    CustOrder = models.ForeignKey(CustOrder, on_delete=models.CASCADE)
    Article = models.ForeignKey(Article, on_delete=models.CASCADE)