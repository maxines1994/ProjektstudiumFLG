"""
Diese Migrations-Datei fuegt alle Unbekannt-Datensaetze (ID = -1) hinzu.
"""

from django.db import migrations
from django.utils import timezone
from gtapp.constants import statuses, bookingcodes
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
        
        #JOGA
        TodoType.objects.create(id=1, title_de = "Auftrag freigeben", description_de ="Bitte geben Sie den Auftrag frei!", group_id=6)
        TodoType.objects.create(id=2, title_de = "Bestand prüfen", description_de ="Bitte prüfen Sie den Bestand", group_id=12)
        TodoType.objects.create(id=3, title_de = "Bestellung erstellen", description_de ="Bitte bestellen Sie die nich vorrätigen Teile bei dem Lieferanten 100!", group_id=12)
        TodoType.objects.create(id=4, title_de = "Wareneingang", description_de ="Bitte führen Sie den Wareingang durch und prüfen Sie dabei die eingetroffenen Teile.", group_id=12)
        TodoType.objects.create(id=5, title_de = "Teilelieferung an Produktion", description_de ="Bitte liefern Sie die Teile an die Produktion!", group_id=12)
        TodoType.objects.create(id=6, title_de = "Hebebühne produzieren", description_de ="Bitte bauen Sie die Hebebühne nach der ANleitung und führen Sie am Ende eine Qualitätsprüfung durch.", group_id=11)
        TodoType.objects.create(id=7, title_de = "Hebebühne an Kundendienst leifern", description_de ="Bitte liefern Sie die Hebebühne an den Kundendienst", group_id=11)
        TodoType.objects.create(id=8, title_de = "Hebebühne an Kunden leifern", description_de ="Bitte liefern Sie die Hebebühne an den Kunden", group_id=6)
        
        #Lieferant 300
        TodoType.objects.create(id=9, title_de = "Bestand prüfen", description_de ="Bitte prüfen Sie den Bestand!", group_id=15)
        TodoType.objects.create(id=10, title_de = "Lieferung versenden", description_de ="Bitte stellen Sie die Box mit den bestellten Teilen fertg und senden Sie diese an JOGA. Denken Sie daran eine E-Mail mit der Box-Nummer an JOGA zu senden.", group_id=15)

        #Bestellung Kunde 1,2,3, Joga
        TodoType.objects.create(id=11, title_de = "Wareneingang buchen", description_de ="Bitte buchen Sie den Wareneingang und führen Sie gleichzeitig eine Qualitätsprüfung durch.", group_id=2)
        TodoType.objects.create(id=12, title_de = "Wareneingang buchen", description_de ="Bitte buchen Sie den Wareneingang und führen Sie gleichzeitig eine Qualitätsprüfung durch.", group_id=3)
        TodoType.objects.create(id=13, title_de = "Wareneingang buchen", description_de ="Bitte buchen Sie den Wareneingang und führen Sie gleichzeitig eine Qualitätsprüfung durch.", group_id=4)
        TodoType.objects.create(id=14, title_de = "Wareneingang buchen", description_de ="Bitte buchen Sie den Wareneingang und führen Sie gleichzeitig eine Qualitätsprüfung durch.", group_id=12)

        #weitere von JOGA
        TodoType.objects.create(id=15, title_de = "Bestellung freigeben", description_de ="Bitte geben Sie die Bestellung frei", group_id=12)

        #Bestellung freigeben Kunden (Kunde 1,2,3)
        TodoType.objects.create(id=16, title_de = "Bestellung freigeben", description_de ="Bitte geben Sie die Bestellung frei", group_id=2)
        TodoType.objects.create(id=17, title_de = "Bestellung freigeben", description_de ="Bitte geben Sie die Bestellung frei", group_id=3)
        TodoType.objects.create(id=18, title_de = "Bestellung freigeben", description_de ="Bitte geben Sie die Bestellung frei", group_id=4)

    dependencies = [
        ('gtapp', '0001_initial'),
        ('gtapp', '0002_insert_translations'),
        ('gtapp', '0003_insert_usergroups'),
        ('gtapp', '0004_insert_statuses'),

    ]

    operations = [
        migrations.RunPython(insert_unknowns),
    ]