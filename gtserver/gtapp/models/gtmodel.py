from django.db import models
from django.contrib.auth.models import User
from gtapp.constants import *
from . import Status, GtModelBasic


class GtModel(GtModelBasic):
    """
    Der Standard-Modeltyp alle Models der Glotrain-App, die ein Statusfeld brauchen.
    Es enthaelt die Methoden set_status() und get_status().
    """

    status = models.ForeignKey(Status,null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    def set_status(self, code: str):
        """
        Aendert den Status eines Objekts. Es muss nur der Status-Code uebergeben werden,
        auf den gewechselt werden soll. Das funktioniert in allen Tabellen, die einen Status haben.
        
        Beispiel:

        myTodo.set_status(TODO_DONE)

        Setzt den Status des Todos in der variable myTodo auf "erledigt".
        """
        try:

            #_meta.model_name ist der name des konkreten Models, das diese Methode aufruft.
            my_table = str(self._meta.model_name).upper
            self.status = Status.objects.get(table=my_table, code=code)
            self.save()

        except ObjectDoesNotExist:
            raise Exception("Status """ + code + """ does not exist for table """ + my_table + "")


    def get_status(self):
        """
        Gibt den aktuellen Status-Code eines Objekts zurueck.
        """
        return self.status.code

