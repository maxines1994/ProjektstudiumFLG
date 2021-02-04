from django.db import models
from .complaint import Complaint
from .supporder import SuppOrder


class SuppComplaint(Complaint):
    """
    Dieses Model enthaelt die Kopfdaten von Lieferanten-Reklamationen.
    """
    class Status(models.TextChoices):

        STANDARD                        = '0', ('Standard')
        ERFASST                         = '1', ('Erfasst')
        IN_REKLAMATION                  = '2', ('In Reklamation') ##Nur für den Lieferanten
        WEITERLEITUNG_AN_PDL            = '3', ('Reklamation an PDL leiten') ##Nur wenn Rekla in PRO erstellt
        REKLAMATION_FREIGEGEBEN         = '4', ('Reklamation freigegeben')
        LIEFERUNG_AN_LIEFERANTEN        = '5', ('Lieferung an Lieferanten')
        BESTANDSPRUEFUNG_AUSSTEHEND     = '6', ('Bestandsprüfung ausstehend')
        LIEFERUNG_AN_PDL                = '7', ('Lieferung an PDL')
        GELIEFERT                       = '8', ('Geliefert')
        ABGESCHLOSSEN                   = '9', ('Abgeschlossen') ##Nur wenn keine Neulieferung

    status = models.CharField(
        max_length = 1,
        choices = Status.choices,
        default = Status.STANDARD,
    )

    supp_order = models.ForeignKey(SuppOrder, on_delete=models.CASCADE)
