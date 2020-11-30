from django.db import models
from . import OrderDet, SuppOrder, Part

class SuppOrderDet(OrderDet):
    """
    This model contains detailed information for every position of a Supplier-Order.
    It inherits most of its fields from the abstract OrderDet-Class.
    """    

    supp_order = models.ForeignKey(SuppOrder, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)