"""
Diese Migrations-Datei fuegt Ubersetzungen hinzu
"""

from django.db import migrations
from django.contrib.auth.models import User, Group, Permission
from gtapp.constants import *
from gtapp.models import Translation
import csv, os

class Migration(migrations.Migration):
    atomic = False
    def insert_translations(apps, schema_editor):
        my_path = os.path.dirname(__file__).replace("\\" ,"/")

        translation_file = my_path + "/translations.csv"
        
        with open(translation_file, encoding='utf-8') as csv_file:

            reader = csv.reader(csv_file, delimiter=';')

            for row in reader:
                if row[0] == '(unbekannt)':
                    Translation.objects.create(id=UNKNOWN, string_de=row[0], string_en=row[1])
                else:
                    Translation.append(english_string=row[1], german_string=row[0])

            csv_file.close()
 
    dependencies = [
        ('gtapp', '0001_initial'),
    ]           
    
    operations = [
        migrations.RunPython(insert_translations),
    ]