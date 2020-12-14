import os
from django.core import management
from django.core.management.base import BaseCommand, CommandError
from gtserver import settings
from gtapp import migrations

class Command(BaseCommand):

    def handle(self, *args, **options):

        def move_files(origin: str, target: str):
            for file in os.listdir(origin):
                #Nur Dateien, die nicht mit "_" anfangen
                if not file.startswith('_'):
                    os.replace(origin + file, target + file)


        migrations_path = os.path.dirname(migrations.__file__).replace("\\" ,"/") + "/"
        temp_path = migrations_path + "_temp/"
        db_name = settings.DATABASES['default']['NAME']
        
        #Datenbank loeschen
        if os.path.exists(db_name):
            os.remove(db_name)
        else:
            print(db_name + " does not exist. Proceeding...")
        
        #0001_initial.py loeschen
        os.remove(migrations_path + '0001_initial.py')
        
        #Alle Dateien im Migrations-Ordner nach _temp verschieben
        move_files(migrations_path, temp_path)

        #Makemigrations
        management.call_command('makemigrations')
        
        #Alle Dateien aus _temp wieder in migrations schieben
        move_files(temp_path, migrations_path)

        #Migrations ausfuehren
        management.call_command('migrate')