from django.db import models
from django.contrib.auth import get_user_model
from . import GtModel, Message
from gtapp.constants import *

class MessageUser(GtModel):
    """
    Dieses Model ordnet die Nachrichten den Usern zu (dem Absender und den Adressaten)
    """
    user_is_sender = models.BooleanField(default=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_trash = models.BooleanField(default=False)

