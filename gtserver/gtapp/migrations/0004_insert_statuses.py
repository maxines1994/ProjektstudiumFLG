"""
Diese Migrations-Datei fuegt alle Status aus der constanty.py in die status-Tabelle ein.
HIER KEINE STATUS MANUELL HINZUFUEGEN. DIES GESCHIEHT NUR IN DER CONSTANS.PY!
"""

from django.db import migrations
from django.utils import timezone
from gtapp.constants import statuses, bookingcodes
from gtapp.constants.general import *
from gtapp.constants.languages import *
from gtapp.models import Status, BookingCode, Translation

class Migration(migrations.Migration):
    atomic = False
    def insert_statuses(apps, schema_editor):
        #Schnapp dir ein item aus constants.py nach dem anderen.
        for item in dir(statuses):
            #Ignoriere alles, was keine Variable ist.
            if not item.startswith("__"): 
                """
                Konstanten fuer Status werden folgendermassen deklariert:
                TABELLE_BESCHREIBUNG = STATUSCODE
                Zum Beispiel:
                CUSTORDERDET_TO_BE_DONE = 'B'
                """
                
                #Erstes Wort des items vor dem ersten '_' ist der Tabellenname
                itemTable = str(item.split('_',1)[0])

                #Alle restlichen Buchstaben sind die Beschreibung. Uebrige '_' werden durch Leerstellen ersetzt
                #und alle Buchstaben werden kleingedruckt.
                itemDescriptionEN = str(item.split('_',1)[1].replace('_', ' ')).casefold()

                #Hol die deutsche Uebersetzung der Statusbeschreibung aus der Translation-Tabelle
                if Translation.objects.filter(string_en=itemDescriptionEN):
                    itemDescriptionDE = Translation.get_translation(to_language=LANG_DE, translate_string=itemDescriptionEN)
                else:
                    itemDescriptionDE = Translation.objects.get(id=UNKNOWN).string_de

                #Das Attribut eines items ist der code des Status
                itemCode = str(getattr(statuses,item))
            
                Status.objects.create(table=itemTable, code=itemCode, description_en=itemDescriptionEN, description_de=itemDescriptionDE)

    def insert_bookingcodes(apps, schema_editor):
        #Schnapp dir ein item aus bookingcodes.py nach dem anderen.
        for item in dir(bookingcodes):
            #Ignoriere alles, was keine Variable ist.
            if not item.startswith("__"):

                #Erstes Wort des items vor dem ersten '_' ist der Tabellenname
                itemBookingcode = str(getattr(bookingcodes,item))   

                #Alle restlichen Buchstaben sind die Beschreibung. Uebrige '_' werden durch Leerstellen ersetzt
                #und alle Buchstaben werden kleingedruckt.            
                itemDescriptionEN = str(item.split('_',1)[1].replace('_', ' ').casefold().title())

                #Hol die deutsche Uebersetzung der Statusbeschreibung aus der Translation-Tabelle
                itemDescriptionDE = ''#Translation.get_translation(to_language=LANG_DE, to_be_translated=itemDescriptionEN)
                #itemDescriptionDE = translator.translate(itemDescriptionEN)


                BookingCode.objects.create(code=itemBookingcode, description_en=itemDescriptionEN, description_de=itemDescriptionDE)

             
    dependencies = [
        ('gtapp', '0001_initial'),
        ('gtapp', '0002_insert_translations'),
        ('gtapp', '0003_insert_usergroups'),
    ]

    operations = [
        migrations.RunPython(insert_statuses),
        migrations.RunPython(insert_bookingcodes),
    ]