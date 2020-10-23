from django.db import models
from django.contrib.auth.models import User
from . import Status

class Order(models.Model):
    """
    This is an abstract template-Class for Supplier-Orders and Customer-Orders.
    It contains the fields, that all types of Orders have in common.
    """

    status = models.ForeignKey(Status,null=True, on_delete=models.SET_NULL)
    order_no = models.CharField(max_length=8)
    price = models.SmallIntegerField()
    issued_on = models.SmallIntegerField()
    delivery_date = models.SmallIntegerField()
    received_on = models.SmallIntegerField()
    memo = models.TextField()
    user = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True