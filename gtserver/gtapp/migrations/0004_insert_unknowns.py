"""
Diese Migrations-Datei fuegt alle Unbekannt-Datensaetze (ID = -1) hinzu.
"""

from django.db import migrations
from django.utils import timezone
from gtapp.constants import *
from gtapp.models import *
from django.contrib.auth.models import Group, User

class Migration(migrations.Migration):
    atomic = False
    def insert_unknowns(apps, schema_editor):
        #unknown_de = Translation.objects.get(id=UNKNOWN).string_de
        #unknown_en = Translation.objects.get(id=UNKNOWN).string_en
        #Article.objects.create(id=UNKNOWN, article_no=0, description=unknown_de)
        #BookingCode.objects.create(id=UNKNOWN, code='',description_en=unknown_en, description_de=unknown_en)
        TodoType.objects.create(id=1, title_de = "Auftrag freigeben", description_de ="Bitte geben Sie den Auftrag frei!", group_id=6)
        TodoType.objects.create(id=2, title_de = "Teile (L300) bestellen", description_de ="Bitte bestellen Sie die Teile für den Auftrag bei dem Lieferanten L300!", group_id=12)
        TodoType.objects.create(id=3, title_de = "Teile prüfen", description_de ="Bitte überprüfen Sie die zugesendeten Teile von dem Lieferanten L300! Bei vorliegenden Mängeln, erstellen Sie eine Reklamation!", group_id=12)
        TodoType.objects.create(id=4, title_de = "Teile an die Produktion senden", description_de ="Bitte senden Sie alle Teile an die Produktion!", group_id=12)
        TodoType.objects.create(id=5, title_de = "Hubwagen bauen", description_de ="Bitte bauen Sie den Hubwagen! Eine Buanleitung finden Sie unter....", group_id=11)
        TodoType.objects.create(id=6, title_de = "Hubwagen prüfen", description_de ="Bitte überprüfen Sie den Hubwagen. Wenn keine Mängel vorliegen leiten Sie diesen an den Kundendienst weiter. Bei vorliegenden Mängel klicken Sie auf den Button [...]", group_id=11)
        TodoType.objects.create(id=7, title_de = "Hubwagen an Kunden senden", description_de ="Bitte senden Sie den Hubwagen an den Kunden.", group_id=6)
             
    dependencies = [
        ('gtapp', '0001_initial'),
        ('gtapp', '0002_insert_translations'),
        ('gtapp', '0003_insert_usergroups'),

    ]

    operations = [
        migrations.RunPython(insert_unknowns),
    ]