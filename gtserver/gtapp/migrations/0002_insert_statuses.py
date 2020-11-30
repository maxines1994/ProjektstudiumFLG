# This is the migration file for all statuses
# DO NOT MANUALLY ADD ANY STATUSES IN THIS FILE. ONLY DO SO IN THE CONSTANTS.PY!
# This migration file will insert all statuses from constants.py into the status-table

from django.db import migrations
from gtapp.constants import statuses
from gtapp.models import Status

class Migration(migrations.Migration):
    atomic = False
    def insert_statuses(apps, schema_editor):
        #Fetch next item in constants.py
        for item in dir(statuses):
            #Ignore anything thats not a variable
            if not item.startswith("__"): 
                #Constants for statuses are declared like this:
                #TABLE_DESCRIPTION = STATUS
                #for example:
                #CUSTORDERDET_TO_BE_DONE = 'B'
                
                #First word of an item before '_' is the Table-name
                itemTable = str(item.split('_',1)[0])

                #All remaining letters are the Description. Remaining '_' are replaced by spaces 
                #and all words start with a capital letter
                itemDescription = str(item.split('_',1)[1].replace('_', ' ').casefold().title())

                #The attribute of the item is the character-code for the Status
                itemStatus = str(getattr(statuses,item))
                
                Status.objects.create(table=itemTable, status=itemStatus, description_en=itemDescription)

    dependencies = [
        ('gtapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_statuses),
    ]