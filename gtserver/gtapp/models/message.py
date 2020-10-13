from django.db import models
from django.contrib.auth.models import User

"""
This model contains all chat-messages, which contain the message itself and timestamps when it was
delivered and received. It also identifies the sending and receiving user.
"""

class Message(models.Model):
    Status = models.CharField(max_length=1)
    Sender =  models.ForeignKey(User,null=True, related_name='sender', on_delete=models.SET_NULL)
    Receiver = models.ForeignKey(User,null=True, related_name='receiver', on_delete=models.SET_NULL)
    DeliveredOn = models.SmallIntegerField()
    ReadOn = models.SmallIntegerField()
    Memo = models.TextField