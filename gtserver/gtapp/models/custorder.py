from django.db import models
from django.contrib.auth.models import User
from . import Order, Customer

class CustOrder(Order):
    """
    Diese Model enthaelt die Kopfdaten der Kundenauftraege.
    """    

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return ("Auftrag " + self.order_no)