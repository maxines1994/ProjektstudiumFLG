from django.db import models
from django.contrib.auth.models import User, Group
from gtapp.constants import *
from . import GtModel

class Message(GtModel):
    """
    Dieses Model enthaelt die einzelnen Nachrichten des Nachrichtensystems. Es speichert die Nachricht selbst,
    Absender und Empfaenger, sowie die Zeitstempel wann sie verschickt, erhalten und gelesen wurde.
    """  
    class Status(models.TextChoices):

        DEFAULT                = '0', ('Standard')
        BEING_COMPOSED         = '1', ('Wird verfasst')
        SENT                   = '2', ('Versendet')
        RECEIVED               = '3', ('Empfangen')
        READ                   = '4', ('Gelesen')  

    text = models.TextField()
    subject = models.CharField(max_length=100)
    sent_on = models.SmallIntegerField()
    sender =  models.ForeignKey(User, default=UNKNOWN, related_name='sender', on_delete=models.SET_DEFAULT)
    receiver = models.ForeignKey(Group, default=UNKNOWN, related_name='receiver', on_delete=models.SET_DEFAULT)

    status = models.CharField(
        max_length = 1,
        choices = Status.choices,
        default = Status.DEFAULT,
    )

