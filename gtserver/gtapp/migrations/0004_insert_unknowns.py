"""
Diese Migrations-Datei fuegt alle Unbekannt-Datensaetze (ID = -1) hinzu.
"""

from django.db import migrations
from django.utils import timezone
from gtapp.constants import statuses, bookingcodes
from gtapp.constants.general import *
from gtapp.constants.languages import *
from gtapp.models import *

class Migration(migrations.Migration):
    atomic = False
    def insert_unknowns(apps, schema_editor):
        unknown_de = Translation.objects.get(id=UNKNOWN).string_de
        unknown_en = Translation.objects.get(id=UNKNOWN).string_en
        Article.objects.create(id=UNKNOWN, article_no=0, description=unknown_de)
        BookingCode.objects.create(id=UNKNOWN, code='',description_en=unknown_en, description_de=unknown_en)

             
    dependencies = [
        ('gtapp', '0001_initial'),
        ('gtapp', '0002_insert_translations'),
        ('gtapp', '0003_insert_usergroups'),

    ]

    operations = [
        migrations.RunPython(insert_unknowns),
    ]