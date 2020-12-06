from django.db import models
from gtapp.models.custorderdet import CustOrderDet
from . import Order, Supplier

class SuppOrder(Order):
    """
    Diese Model enthaelt die Kopfdaten der Lieferantenbestellungen.
    """   

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    
    def __str__(self):
        return ("Bestellung " + self.order_no)