from django.db import models
from . import Container, CustOrderDet

class CustContainer(Container):
    """
    This is model contains the information about Containers that are used to ship lifting-platforms
    to the costumer. They are used to map the container via Barcode to the Costumer-Order-Details.
    It inherits most of its fields from the abstract Container-Class
    """    

    cust_order_det = models.ForeignKey(CustOrderDet, on_delete=models.CASCADE)