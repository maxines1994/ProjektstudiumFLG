from django.db import models
from . import Status, CustOrderDet

"""
This model contains all information about Todos. It identifies the User, that gets the todo,
the Todo-Text, as well as the mapping to the Customer-Order-Details.
"""


class Todo(models.Model):
    Status = models.ForeignKey(Status,null=True, on_delete=models.SET_NULL)
    UserID = models.SmallIntegerField()
    CustOrderDetID = models.SmallIntegerField()
    Memo = models.TextField()
    FinishedOn = models.SmallIntegerField()