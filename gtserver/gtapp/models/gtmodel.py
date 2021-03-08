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

    def get_creation_user(self):
        return self._creation_user

    def get_update_user(self):
        return self._update_user

    def gtmodel_to_foreign_field_name(model: models.Model):
        """
        Erwartet ein Model und liefert die uebliche Fremdschluesselbezeichnung zurueck
        Bsp: CustOrderDet => cust_order_det oder SuppComplaintDet => supp_complaint_det
        Funktioniert nur mit Models die irgendwo "order", "complaint" oder "det" enthalten.
        """
        # Entferne alle Grossbuchstaben aus dem Modelnamen
        my_fieldname  = model.__name__.casefold()
        # Ermittle die Position des ersten Unterstrichs. Also nach "order" oder "complaint"
        # je nachdem, welcher Begriff im Modelnamen vorkommt
        order_complaint_pos = my_fieldname.find("order") if my_fieldname.find("order") >= 0 else my_fieldname.find("complaint")
        # Fuege an der gefundenen Stelle "_" ein
        my_fieldname = GtModel.insert_underscore(my_fieldname, order_complaint_pos)    
        # Falls das Model ein "det" enthaelt muss hier ein weiterer Unterstrich eingefuegt werden, sonst nicht.
        det_pos = my_fieldname.find("det")
        my_fieldname = GtModel.insert_underscore(my_fieldname, det_pos) if det_pos >= 0 else my_fieldname
        
        return my_fieldname

    def insert_underscore(string, index):
        """
        Fuegt an der stelle "index" einen "_" ein und gibt den string wieder zurueck. 
        """
        return string[:index] + '_' + string[index:]