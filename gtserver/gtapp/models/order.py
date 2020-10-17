from django.db import models
from django.contrib.auth.models import User
from . import Status

"""
This is an abstract template-Class for Supplier-Orders and Customer-Orders.
It contains the fields, that all types of Orders have in common.
"""

class Order(models.Model):
    Status = models.ForeignKey(Status,null=True, on_delete=models.SET_NULL)
    OrderNo = models.CharField(max_length=8)
    Price = models.SmallIntegerField()
    IssuedOn = models.SmallIntegerField()
    DeliveryDate = models.SmallIntegerField()
    ReceivedOn = models.SmallIntegerField()
    Memo = models.TextField()
    User = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True