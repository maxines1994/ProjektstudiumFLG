from django.db import models
from .custorderdet import CustOrderDet

"""
This model contains all information about Todos. It identifies the User, that gets the todo,
the Todo-Text, as well as the mapping to the Customer-Order-Details.
"""


class Todo(models.Model):
    Status = models.CharField(max_length=1)
    UserID = models.SmallIntegerField()
    CustOrderDetID = models.SmallIntegerField()
    Memo = models.TextField()
    FinishedOn = models.SmallIntegerField()