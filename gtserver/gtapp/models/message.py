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

        ERFASST              = 1, ('Erfasst')
        VERSENDET            = 2, ('Versendet')
        EMPFANGEN            = 3, ('Empfangen')
        GELESEN              = 4, ('Gelesen')  

    text = models.TextField()
    subject = models.CharField(max_length=100)
    sent_on = models.SmallIntegerField()
    read_on = models.SmallIntegerField(null=True)
    sender =  models.ForeignKey(User, null=True, related_name='sender', on_delete=models.SET_NULL)
    receiver = models.ForeignKey(Group, null=True, related_name='receiver', on_delete=models.SET_NULL)

    status = models.CharField(
        max_length = 2,
        choices = Status.choices,
        default = Status.ERFASST,
    )

