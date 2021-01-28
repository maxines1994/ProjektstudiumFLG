"""
Diese Migrations-Datei fuegt alle Gruppen und Nutzer hinzu.
"""
from django import apps
from django.db import migrations, models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from gtserver import settings
from gtapp.constants import *
from gtapp.constants import groups
from gtapp.models import *
from gtapp import models
from gtapp.models import LiveSettings

class Migration(migrations.Migration):
    atomic = False

    def insert_permissions(apps, schema_editor):
        from django.apps import apps
        from django.contrib.auth.management import create_permissions
        
        for app_config in apps.get_app_configs():
            app_config.models_module = True
            create_permissions(app_config=app_config,verbosity=0)
            apps.models_module = None


    def insert_usergroups(apps, schema_editor):
        """
        Fuege die User, Gruppen ihre Rechte und Organisationseinheiten hinzu
        """

        #Deklariere Listen fuer die Gruppen und deren Codes aus den Konstanten
        group_list = []
        code_list  = []

        def get_content_type_ids_of_models(*args):
            my_list = []
            for item in args:
                item_name = item.__name__.casefold()
                my_list.append(ContentType.objects.get(model=item_name).id)

            return my_list

        def get_group_permissions(group: Group):
            """
            Gibt eine Liste an Rechten zurueck, die der uebergebenen Gruppe zugeordnet ist
            """
            app_models         = []
            can_view_only      = []
            can_change         = []
            perms_list         = []

            VIEW    = 'view'
            CHANGE  = 'change'

            for ct in ContentType.objects.all():
                app_models.append(ct.model_class())

            def get_perms(models_list: list, permission_type: str):
                """
                Gibt alle Rechte eines bestimmten Typs fuer ein Model zurueck.

                Beispiel: get_perms(models_list=myList, permission_type='view')
                Gibt alle "view"-Rechte fuer die uebergebenen Models zurueck
                """
                perm_list = []

                #Wer aendern darf, der darf auch sehen, deshalb wird in diesem Fall die permission_type nicht eingeschraenkt
                if permission_type == CHANGE:
                    permission_type = ''

                #Queryset mit den IDs aller fraglichen Rechte
                qry_permission_ids = Permission.objects.filter(content_type__in=models_list, codename__contains=permission_type).values_list('id', flat=True)

                for item in qry_permission_ids:
                    #Hier werden die IDs in einer Schleife einer integer-list angefuegt.
                    perm_list.append(item)
                return perm_list
            
            if group.name == GAME_MASTER:
                for model in app_models:
                    can_change.append(get_content_type_ids_of_models(model)[0])
  
            if group.name == MANAGEMENT:
                for model in app_models:
                    can_view_only.append(get_content_type_ids_of_models(model)[0])
        
            if group.name == CUSTOMERS:
                can_view_only   = get_content_type_ids_of_models(CustContainer)
                can_change      = get_content_type_ids_of_models(CustOrder, CustOrderDet, CustComplaint, CustComplaintDet,Message, Todo)

            if group.name == CUSTOMER_SERVICE:
                can_view_only   = get_content_type_ids_of_models(Article, ArtiPart, Part, CustContainer)
                can_change      = get_content_type_ids_of_models(CustOrder, CustOrderDet, CustComplaint, CustComplaintDet, Todo, Message,)

            if group.name == INTERNAL_SERVICE:
                #can_view_only   = get_content_type_ids_of_models
                can_change      = get_content_type_ids_of_models(Todo, Message, CustContainer, SuppContainer)

            if group.name == PRODUCTION_SERVICE:
                can_view_only   = get_content_type_ids_of_models(CustOrder, CustOrderDet, CustComplaint, CustComplaintDet, Article, ArtiPart, Part, SuppContainer)
                can_change      = get_content_type_ids_of_models(SuppOrder, SuppOrderDet, SuppComplaint, SuppComplaintDet, Todo, Message, Stock, StockMovement)

            if group.name == PRODUCTION:
                can_view_only   = get_content_type_ids_of_models(CustOrder, CustOrderDet, CustComplaint, CustComplaintDet, SuppComplaint, SuppComplaintDet)
                can_change      = get_content_type_ids_of_models(Todo, Message)

            if group.name == SUPPLIERS:
                can_view_only   = get_content_type_ids_of_models(SuppContainer)
                can_change      = get_content_type_ids_of_models(SuppOrder, SuppOrderDet, SuppComplaint, SuppComplaintDet, SuppContainer, Todo)

            perms_list = get_perms(can_view_only, VIEW)
            perms_list = perms_list + get_perms(can_change, CHANGE)        
            
            #Stelle sicher, dass keine Rechte doppelt in der Liste vorkommen
            distinct_perms = []
            [distinct_perms.append(x) for x in perms_list if x not in distinct_perms]
            
            return distinct_perms    

        #Schnapp dir ein item aus groups.py nach dem anderen.
        for item in dir(groups):
        #Ignoriere alles, was keine Variable ist.
            if not item.startswith("__"):
                #Wenn der Name der Konstanten keinen "CODE" enthaelt, ist es der volle Gruppenname, wie "management" oder "customer service"
                #Speichere den Eintrag in der Gruppenliste
                if item.find('CODE') == UNKNOWN:
                    group_list.append(item)
                #Sonst ist es die Konstante des Kurzels. Speichere den Eintrag in der Codeliste
                else:
                    code_list.append(item)

        #Initialisiere Index-Zähler
        i = 0                    
        for item in group_list:
            #Englischer Name ist einfach nur das Attribut des Items aus der Gruppenliste
            my_name_en = str(getattr(groups, group_list[i]))
            #Uebersetze den Namen ins Deutsche
            my_name_de = Translation.get_translation(to_language=LANG_DE, translate_string=my_name_en)
            """
            Der Englische Code ist das Attribut des Items aus der Codeliste. Django liest die Items aus einer Datei immer in alphabetischer Reihenfolge ein.
            Die zusammengehoerenden Paare von code_list und group_list haben also den gleichen Index, deswegen wird in dieser Schleife nur 1 Index fuer beide Listen verwendet.
            Beispiel: Eintrag fuer MANAGEMENT in group_list hat den gleichen Index wie MANAGEMENT_CODE in code_list
            """
            my_code_en = str(getattr(groups, code_list[i]))
            #Uebersetze Code ins Deutsche
            my_code_de = Translation.get_translation(to_language=LANG_DE, translate_string=str(getattr(groups,code_list[i])))

            #Erzeuge Gruppe
            my_group = Group(name=my_name_en, name_de=my_name_de, code=my_code_en, code_de=my_code_de)
            my_group.save()

            #if my_group.name == MANAGEMENT:
            #Weise der Gruppe die Rechte zu
            my_perms = get_group_permissions(my_group)
            my_group.permissions.set(my_perms)
            #Zaehle den Index-Zaehler hoch
            i += 1

        #Rechte sammeln
        #perms_mg   = Permission.objects.filter(id=1).first()
        #(content_type__in=ContentType.objects.filter(app_label='gtapp'))
        #Gruppen mit vorhin gesammelten Rechten

        #User
        """
        Erstelle die Menge an Nutzern, die in constants.players hinterlegt ist
        und ordne sie ihren Gruppen zu. Username und password sind nummeriert und
        starten mit der Gruppen-Abkuerzung.

        Beispiel: Der zweite Benutzer der Produktionsgruppe hat als 
        Benutzername und Password "PRO2"
        """

        #Superuser erstellen
        if (settings.DEBUG):
            newUser = User(username=ADMIN, is_superuser=True, is_staff=True, is_active=True)
            newUser.set_password(ADMIN)
            newUser.save()
            print("Superuser '"+ ADMIN + "' was created.")
        else:
            print("Superuser was not created because the debug flag in settings.py is not set.")

        #Leitungsteam
        for number in range(1, PLAYER_AMOUNT_MANAGEMENT + 1):
            
            my_name_de = Translation.get_translation(to_language=LANG_DE, translate_string=MANAGEMENT_CODE)
            newUser = User(username=my_name_de + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.set_password(my_name_de + str(number))
            newUser.save()
            my_group = Group.objects.get(name=MANAGEMENT)
            newUser.groups.add(my_group)
            my_group = Group.objects.get(name=JOGA)
            newUser.groups.add(my_group)
             
        #Kunden
        for number in range(1, PLAYER_AMOUNT_CUSTOMERS + 1):
            my_name_de = Translation.get_translation(to_language=LANG_DE, translate_string=CUSTOMERS_CODE)
            newUser = User(username=my_name_de + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.set_password(my_name_de + str(number))
            newUser.save()
            my_group = Group.objects.get(name=CUSTOMERS)
            newUser.groups.add(my_group)
            if number == 1:
                my_group = Group.objects.get(name=C1)
            if number == 2:
                my_group = Group.objects.get(name=C2)
            if number == 3:
                my_group = Group.objects.get(name=C3)
            if number <= 3:
                newUser.groups.add(my_group)

        #Kundendienst
        for number in range(1, PLAYER_AMOUNT_CUSTOMER_SERVICE + 1):
            my_name_de = Translation.get_translation(to_language=LANG_DE, translate_string=CUSTOMER_SERVICE_CODE)
            newUser = User(username=my_name_de + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.set_password(my_name_de + str(number))
            newUser.save()
            my_group = Group.objects.get(name=CUSTOMER_SERVICE)
            newUser.groups.add(my_group)
            my_group = Group.objects.get(name=JOGA)
            newUser.groups.add(my_group)

        #Interne Dienstleistung
        for number in range(1, PLAYER_AMOUNT_INTERNAL_SERVICE + 1):
            my_name_de = Translation.get_translation(to_language=LANG_DE, translate_string=INTERNAL_SERVICE_CODE)
            newUser = User(username=my_name_de + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.set_password(my_name_de + str(number))
            newUser.save()
            my_group = Group.objects.get(name=INTERNAL_SERVICE)
            newUser.groups.add(my_group)
            my_group = Group.objects.get(name=JOGA)
            newUser.groups.add(my_group)

        #Produktionsdienstleistung
        for number in range(1, PLAYER_AMOUNT_PRODUCTION_SERVICE + 1):
            my_name_de = Translation.get_translation(to_language=LANG_DE, translate_string=PRODUCTION_SERVICE_CODE)
            newUser = User(username=my_name_de + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.set_password(my_name_de + str(number))
            newUser.save()
            my_group = Group.objects.get(name=PRODUCTION_SERVICE)
            newUser.groups.add(my_group)
            my_group = Group.objects.get(name=JOGA)
            newUser.groups.add(my_group)

        #Produktion
        for number in range(1, PLAYER_AMOUNT_PRODUCTION + 1):
            my_name_de = Translation.get_translation(to_language=LANG_DE, translate_string=PRODUCTION_CODE)
            newUser = User(username=my_name_de + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.set_password(my_name_de + str(number))
            newUser.save()
            my_group = Group.objects.get(name=PRODUCTION)
            newUser.groups.add(my_group)
            my_group = Group.objects.get(name=JOGA)
            newUser.groups.add(my_group)

        #Lieferanten
        for number in range(1, PLAYER_AMOUNT_SUPPLIERS+ 1):
            my_name_de = Translation.get_translation(to_language=LANG_DE, translate_string=SUPPLIERS_CODE)
            newUser = User(username=my_name_de + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.set_password(my_name_de + str(number))
            newUser.save()
            my_group = Group.objects.get(name=SUPPLIERS)
            newUser.groups.add(my_group)

            if number == 1:
                my_group = Group.objects.get(name=S100)
            if number == 2:
                my_group = Group.objects.get(name=S200)
            if number == 3:
                my_group = Group.objects.get(name=S300)
            if number <= 3:
                newUser.groups.add(my_group)

        #Spielleitung
        for number in range(1, PLAYER_AMOUNT_GAME_MASTER + 1):
            my_name_de = Translation.get_translation(to_language=LANG_DE, translate_string=GAME_MASTER_CODE)
            newUser = User(username=my_name_de + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.set_password(my_name_de + str(number))
            newUser.save()
            my_group = Group.objects.get(name=GAME_MASTER)
            newUser.groups.add(my_group)
        
        #Einstellungen
        LiveSettings.load()
        print("Livesettings initialisiert!")

    dependencies = [
        ('gtapp', '0001_initial'),  
        ('gtapp', '0002_insert_translations'),
    ]           
    
    operations = [
        migrations.RunPython(insert_permissions),
        migrations.RunPython(insert_usergroups),
    ]
    