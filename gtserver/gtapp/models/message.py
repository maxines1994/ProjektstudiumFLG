from django.db import models
from django.contrib.auth.models import User
from . import Status

class Message(models.Model):
    """
    This model contains all chat-messages, which contain the message itself and timestamps when it was
    delivered and received. It also identifies the sending and receiving user.
    """    

    status = models.ForeignKey(Status,null=True, on_delete=models.SET_NULL)
    sender =  models.ForeignKey(User,null=True, related_name='sender', on_delete=models.SET_NULL)
    receiver = models.ForeignKey(User,null=True, related_name='receiver', on_delete=models.SET_NULL)
    sent_on = models.SmallIntegerField()
    received_on = models.SmallIntegerField()
    read_on = models.SmallIntegerField()
    text = models.TextField