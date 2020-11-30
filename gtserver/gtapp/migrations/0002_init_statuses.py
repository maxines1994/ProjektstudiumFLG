# This is the migration file for all statuses
# DO NOT MANUALLY ADD ANY STATUS IN THIS FILE. ONLY DO SO IN THE CONSTANTS.PY!
# This migration file will insert all statuses from constants.py into the status-table

from django.db import migrations
from gtapp import constants
from gtapp.models import Status

class Migration(migrations.Migration):

    def Init_Status(apps, schema_editor):
        #Fetch next item in constants.py
        for item in dir(constants):
            #Ignore anything thats not a variable
            if not item.startswith("__"): 
                #Constants for statuses are declared like this:
                #TABLE_DESCRIPTION = STATUS
                #for example:
                #CUSTORDERDET_TO_BE_DONE = 'B'
                
                #First word of an item-name before '_' is the Table-name
                itemTable = str(item.split('_',1)[0])

                #All remaining letters are the Description. Remaining '_' are replaced by spaces 
                #and all words start with a capital letter
                itemDescription = str(item.split('_',1)[1].replace('_', ' ').casefold().title())

                #The attribute of the item is the character-code for the Status
                itemStatus = str(getattr(constants,item))
                
                Status.objects.create(Table=itemTable, Status=itemStatus, Description=itemDescription)

    dependencies = [
        ('gtapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(Init_Status),
    ]

