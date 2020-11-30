from django.db import models
from . import Status, CustOrderDet

class Todo(models.Model):
    """
    This model contains all information about Todos. It identifies the User, that gets the todo,
    the Todo-Text, as well as the mapping to the Customer-Order-Details.
    """

    status = models.ForeignKey(Status,null=True, on_delete=models.SET_NULL)
    user = models.SmallIntegerField()
    cust_order_det = models.SmallIntegerField()
    memo = models.TextField()
    finished_on = models.SmallIntegerField()