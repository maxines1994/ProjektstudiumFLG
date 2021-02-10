from django.db import models
from django.contrib.auth.models import User
from gtapp.constants import *
from django.contrib import admin
from crum import get_current_user
from .timer import Timers
from django.apps import apps

class GtModel(models.Model):
    """
    Der Modeltyp für alle Models der Glotrain-App. Es erweitert das Standard-Model von Django um Zeitstempel fuer Anlage- und
    Update-Zeitpunkt und speichert welcher User den Datensatz angelegt und zuletzt geupdatet hat. Das Model nutzt dazu erweiterte
    Methoden save() zum Speichern und create() zum Anlegen von Datensaetzen. 
    """
    _creation_date = models.DateTimeField(auto_now_add=True)
    _creation_gameday = models.SmallIntegerField(auto_created=True, default=0)
    _creation_user = models.ForeignKey(User, related_name='%(class)s_creation_user', null=True, on_delete=models.SET_NULL)
    _update_date = models.DateTimeField(auto_now=True)
    _update_gameday = models.SmallIntegerField(null=True)
    _update_user = models.ForeignKey(User, related_name='%(class)s_update_user', null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Speichert den aktuellen User und Spieltag in _creation_user/_update_user bzw. _creation_gameday/_update_gameday
        """
        user = get_current_user()
        gameday = Timers.get_current_day()
        #Ist noch kein Primaerschluessel vergeben, wird der Datensatz erstmalig angelegt
        if not self.pk:
            self._creation_user = user
            self._creation_gameday = gameday

        self._update_user = user
        self._update_gameday = gameday
        super().save(*args, **kwargs)

    def str_to_gtmodel(string: str):
        """
        Erwartet den Namen eines Models als String und liefert das Model zurück
        """
        return apps.get_model(app_label='gtapp', model_name=string)
