from django.db import models
from django.contrib.auth.models import User
from gtapp.constants import *
from django.contrib import admin

class GtModelBasic(models.Model):
    """
    Der Basis-Modeltyp für alle Models der Glotrain-App. Es erweitert das Standard-Model von Django um Zeitstempel fuer Anlage- und
    Update-Zeitpunkt und speichert welcher User den Datensatz angelegt und zuletzt geupdatet hat. Das Model nutzt dazu erweiterte
    Methoden save() zum Speichern und create() zum Anlegen von Datensaetzen. 
    """
    _creation_date = models.DateTimeField(auto_now_add=True)
    _creation_user = models.ForeignKey(User, related_name='%(class)s_creation_user',null=True, on_delete=models.SET_NULL)
    _update_date = models.DateTimeField(auto_now=True)
    _update_user = models.ForeignKey(User, related_name='%(class)s_update_user',null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        #Hier muss noch eine Methode gefunden werden um an dieser Stelle den User zu holen, der diese Methode aufruft,
        #optimalerweise ohne ihn explizit uebergeben zu muessen
       # self._update_user = user
        super().save(*args, **kwargs)


    #Hier fehlen noch create()-Methoden, die den Standard ueberschreiben