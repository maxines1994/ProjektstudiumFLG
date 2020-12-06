"""
Diese Migrations-Datei fuegt alle Gruppen und Nutzer hinzu.
"""

from django.db import migrations, models
from django.contrib.auth.models import User, Group, Permission
from gtapp.constants import *
from gtapp.models import *

class Migration(migrations.Migration):
    atomic = False

    def insert_usergroups(apps, schema_editor):
        """
        Fuege die User, Gruppen und Organisationseinheiten hinzu
        """
        #Gruppen
        group_mg    = Group.objects.create(name=MANAGEMENT)
        group_c     = Group.objects.create(name=CUSTOMERS)
        group_cs    = Group.objects.create(name=CUSTOMER_SERVICE)
        group_its   = Group.objects.create(name=INTERNAL_SERVICE)
        group_prs   = Group.objects.create(name=PRODUCTION_SERVICE)
        group_pro   = Group.objects.create(name=PRODUCTION)
        group_sup   = Group.objects.create(name=SUPPLIERS)
        group_gm    = Group.objects.create(name=GAME_MASTER)

        group_mg.save()
        group_c.save()
        group_cs.save()
        group_its.save()
        group_prs.save()
        group_pro.save()
        group_sup.save()
        group_gm.save()

        #Organisationseinheiten
        OrgaUnit.objects.create(group=group_mg, code=MANAGEMENT_CODE, name_de=Translation.get_translation(to_language=LANG_DE, translate_string=MANAGEMENT))
        OrgaUnit.objects.create(group=group_c, code=CUSTOMERS_CODE, name_de=Translation.get_translation(to_language=LANG_DE, translate_string=CUSTOMERS))
        OrgaUnit.objects.create(group=group_cs, code=CUSTOMER_SERVICE_CODE, name_de=Translation.get_translation(to_language=LANG_DE, translate_string=CUSTOMER_SERVICE))
        OrgaUnit.objects.create(group=group_its, code=INTERNAL_SERVICE_CODE, name_de=Translation.get_translation(to_language=LANG_DE, translate_string=INTERNAL_SERVICE))
        OrgaUnit.objects.create(group=group_prs, code=PRODUCTION_SERVICE_CODE, name_de=Translation.get_translation(to_language=LANG_DE, translate_string=PRODUCTION_SERVICE))
        OrgaUnit.objects.create(group=group_pro, code=PRODUCTION_CODE, name_de=Translation.get_translation(to_language=LANG_DE, translate_string=PRODUCTION))
        OrgaUnit.objects.create(group=group_sup, code=SUPPLIERS_CODE, name_de=Translation.get_translation(to_language=LANG_DE, translate_string=SUPPLIERS))
        OrgaUnit.objects.create(group=group_gm, code=GAME_MASTER_CODE, name_de=Translation.get_translation(to_language=LANG_DE, translate_string=GAME_MASTER))
        
        
        #User
        """
        Erstelle die Menge an Nutzern, die in constants.players hinterlegt ist
        und ordne sie ihren Gruppen zu. Username und password sind nummeriert und
        starten mit der Gruppen-Abkuerzung.

        Beispiel: Der zweite Benutzer der Produktionsgruppe hat als 
        Benutzername und Password "PRO2"
        """

        #Leitungsteam
        for number in range(1, PLAYER_AMOUNT_MANAGEMENT + 1):
            newUser = User(username=MANAGEMENT_CODE + str(number), password=MANAGEMENT_CODE + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.save()
            newUser.groups.add(group_mg)
        
        #Kunden
        for number in range(1, PLAYER_AMOUNT_CUSTOMERS + 1):
            newUser = User(username=CUSTOMERS_CODE + str(number), password=CUSTOMERS_CODE + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.save()
            newUser.groups.add(group_c)

        #Kundendienst
        for number in range(1, PLAYER_AMOUNT_CUSTOMER_SERVICE + 1):
            newUser = User(username=CUSTOMER_SERVICE_CODE + str(number), password=CUSTOMER_SERVICE_CODE + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.save()
            newUser.groups.add(group_cs)

        #Interne Dienstleistung
        for number in range(1, PLAYER_AMOUNT_INTERNAL_SERVICE + 1):
            newUser = User(username=INTERNAL_SERVICE_CODE + str(number), password=INTERNAL_SERVICE_CODE + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.save()
            newUser.groups.add(group_its)

        #Produktionsdienstleistung
        for number in range(1, PLAYER_AMOUNT_PRODUCTION_SERVICE + 1):
            newUser = User(username=PRODUCTION_SERVICE_CODE + str(number), password=PRODUCTION_SERVICE_CODE + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.save()
            newUser.groups.add(group_prs)

        #Produktion
        for number in range(1, PLAYER_AMOUNT_PRODUCTION + 1):
            newUser = User(username=PRODUCTION_CODE + str(number), password=PRODUCTION_CODE + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.save()
            newUser.groups.add(group_pro)

        #Lieferanten
        for number in range(1, PLAYER_AMOUNT_SUPPLIERS+ 1):
            newUser = User(username=SUPPLIERS_CODE + str(number), password=SUPPLIERS_CODE + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.save()
            newUser.groups.add(group_sup)

        #Spielleitung
        for number in range(1, PLAYER_AMOUNT_GAME_MASTER + 1):
            newUser = User(username=GAME_MASTER_CODE + str(number), password=GAME_MASTER_CODE + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.save()
            newUser.groups.add(group_gm)
    
    dependencies = [
        ('gtapp', '0001_initial'),  
        ('gtapp', '0002_insert_translations'),
    ]           
    
    operations = [
        migrations.RunPython(insert_usergroups),
    ]