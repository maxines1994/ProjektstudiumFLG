from django.db import models
from django.contrib.auth.models import User
from . import GtModel

class Order(GtModel):
    """
    Das ist eine Abstrakte Klasse und dient als Vorlage fuer Kopfdaten der Bestellungen und Auftraege.
    """

    order_no = models.CharField(max_length=8)
    price = models.SmallIntegerField()
    issued_on = models.SmallIntegerField()
    delivery_date = models.SmallIntegerField()
    received_on = models.SmallIntegerField()
    memo = models.TextField()
    user = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True
