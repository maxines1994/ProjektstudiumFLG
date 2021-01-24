from django.db import models
from gtapp.models.custorderdet import CustOrderDet
from . import Order, Supplier, CustOrder

class SuppOrder(Order):
    """
    Diese Model enthaelt die Kopfdaten der Lieferantenbestellungen.
    """   

    cust_order_det = models.ForeignKey(CustOrderDet, on_delete=models.CASCADE, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    
    def __str__(self):
        return ("Bestellung " + self.order_no)