from django.db import models
from django.contrib.auth.models import User, Group
from gtapp.constants import *
from . import GtModel

class Message(GtModel):
    """
    Dieses Model enthaelt die einzelnen Nachrichten des Nachrichtensystems. Es speichert die Nachricht selbst,
    Absender und Empfaenger, sowie die Zeitstempel wann sie verschickt, erhalten und gelesen wurde.
    """    

    text = models.TextField()
    subject = models.CharField(max_length=100)
    sent_on = models.SmallIntegerField()
    sender =  models.ForeignKey(User,default=UNKNOWN, related_name='sender', on_delete=models.SET_DEFAULT)
    receiver = models.ForeignKey(Group,default=UNKNOWN, related_name='receiver', on_delete=models.SET_DEFAULT)

