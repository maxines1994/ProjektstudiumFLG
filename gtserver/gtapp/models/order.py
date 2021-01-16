from django.db import models
from django.contrib.auth.models import User
from . import GtModel

class Order(GtModel):
    """
    Das ist eine Abstrakte Klasse und dient als Vorlage fuer Kopfdaten der Bestellungen und Auftraege.
    """

    order_no = models.CharField(max_length=8)
    price = models.SmallIntegerField(null=True)
    issued_on = models.SmallIntegerField()
    delivery_date = models.SmallIntegerField()
    received_on = models.SmallIntegerField(null=True)
    memo = models.TextField(null=True)
    user = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    external_system = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
