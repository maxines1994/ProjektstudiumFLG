from django.db import models
from . import GtModel

class MessageTemplate(GtModel):
    """
    Dieses Model enthaelt die Templates fuer Nachrichten. Hier koennen Betreff und Text von Nachrichten
    eines bestimmten Typs mit Platzhaltern gespeichert werden.
    """    

    text = models.TextField
    subject = models.CharField(max_length=100)