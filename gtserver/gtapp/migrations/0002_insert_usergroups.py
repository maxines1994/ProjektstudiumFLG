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
import hashlib

class Migration(migrations.Migration):
    atomic = False

    def insert_permissions(apps, schema_editor):
        from django.apps import apps
        from django.contrib.auth.management import create_permissions
        
        for app_config in apps.get_app_configs():
            app_config.models_module = True
            create_permissions(app_config=app_config, verbosity=0)
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
            
            # if group.name == SPIELLEITUNG:
            #     can_change      = get_content_type_ids_of_models()
  
            if group.name == LEITUNGSTEAM:
                can_change      = get_content_type_ids_of_models(Message)
        
            if group.name == KUNDEN:
                can_view_only   = get_content_type_ids_of_models(CustContainer)
                can_change      = get_content_type_ids_of_models(CustOrder, CustOrderDet, CustComplaint, CustComplaintDet, Message, Task)

            if group.name == KUNDENDIENST:
                can_view_only   = get_content_type_ids_of_models(Article, ArtiPart, Part, CustContainer)
                can_change      = get_content_type_ids_of_models(CustOrder, CustOrderDet, CustComplaint, CustComplaintDet, Task, Message, )

            if group.name == INTERNE_DIENSTLEISTUNG:
                #can_view_only   = get_content_type_ids_of_models
                can_change      = get_content_type_ids_of_models(Task, Message, CustContainer, SuppContainer)

            if group.name == PRODUKTIONSDIENSTLEISTUNG:
                can_view_only   = get_content_type_ids_of_models(CustOrderDet, CustComplaint, CustComplaintDet, Article, ArtiPart, Part, SuppContainer)
                can_change      = get_content_type_ids_of_models(SuppOrder, SuppOrderDet, SuppComplaint, SuppComplaintDet, PermManufacturingList, Task, Message, Stock, StockMovement)

            if group.name == PRODUKTION:
                can_view_only   = get_content_type_ids_of_models(CustOrder, CustOrderDet, CustComplaint, CustComplaintDet, PermManufacturingList, SuppComplaint, SuppComplaintDet, ProductionSteps)
                can_change      = get_content_type_ids_of_models(Task, Message, SuppContainer, CustContainer)

            if group.name == LIEFERANTEN:
                can_view_only   = get_content_type_ids_of_models(SuppContainer)
                can_change      = get_content_type_ids_of_models(SuppOrder, SuppOrderDet, SuppComplaint, SuppComplaintDet, SuppContainer, Message, Task, Stock, StockMovement)

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
                #Wenn der Name der Konstanten keinen "CODE" enthaelt, ist es der volle Gruppenname, wie "LEITUNGSTEAM" oder "customer service"
                #Speichere den Eintrag in der Gruppenliste
                if item.find('CODE') == UNKNOWN:
                    group_list.append(item)
                #Sonst ist es die Konstante des Kurzels. Speichere den Eintrag in der Codeliste
                else:
                    code_list.append(item)

        #Initialisiere Index-Zähler
        i = 0                    
        for item in group_list:
            #Name ist einfach nur das Attribut des Items aus der Gruppenliste
            my_name = str(getattr(groups, group_list[i]))
            """
            Der Code ist das Attribut des Items aus der Codeliste. Django liest die Items aus einer Datei immer in alphabetischer Reihenfolge ein.
            Die zusammengehoerenden Paare von code_list und group_list haben also den gleichen Index, deswegen wird in dieser Schleife nur 1 Index fuer beide Listen verwendet.
            Beispiel: Eintrag fuer LEITUNGSTEAM in group_list hat den gleichen Index wie LEITUNGSTEAM_CODE in code_list
            """
            my_code = ''
            for item in code_list:
                if item == group_list[i] + '_CODE':
                    my_code = str(getattr(groups, item))

            #Erzeuge Gruppe
            my_group = Group(name=my_name, code=my_code)
            my_group.save()

            #if my_group.name == LEITUNGSTEAM:
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

        #Spielleitung
        # ID=1
        my_name = SPIELLEITUNG_CODE
        newUser = User(username=my_name, is_superuser=False, is_staff=False, is_active=True)
        newUser.set_password(str(int(hashlib.sha256(newUser.username.encode('utf-8')).hexdigest(), 16) % 10**4))
        newUser.save()
        my_group = Group.objects.get(name=SPIELLEITUNG)
        newUser.groups.add(my_group)
        newUser.groups.add(Group.objects.get(name=SPIELLEITUNG))

        #Superuser erstellen
        if (settings.DEBUG):
            newUser = User(username=ADMIN, is_superuser=True, is_staff=True, is_active=True)
            newUser.set_password(ADMIN)
            newUser.save()
            print("Superuser '"+ ADMIN + "' was created.")
        else:
            print("Superuser was not created because the debug flag in settings.py is not set.")

        #Geschäftsleitung
        for number in range(0, PLAYER_AMOUNT_LEITUNGSTEAM + 1):
            
            my_name = LEITUNGSTEAM_CODE
            newUser = User(username=my_name + '-'  + str(number), is_superuser=False, is_staff=False, is_active=True)
            if number==0:
                newUser.username=my_name + '-' + SPIELLEITUNG_CODE
            newUser.set_password(str(int(hashlib.sha256(newUser.username.encode('utf-8')).hexdigest(), 16) % 10**4))
            newUser.save()
            my_group = Group.objects.get(name=LEITUNGSTEAM)
            newUser.groups.add(my_group)
            my_group = Group.objects.get(name=JOGA)
            newUser.groups.add(my_group)
            if number==0:
                newUser.groups.add(Group.objects.get(name=SPIELLEITUNG))
             
        #Kunden
        for customer in range(1, 4):
            for number in range(0, PLAYER_AMOUNT_KUNDEN + 1):
                my_name = KUNDEN_CODE + str(customer)
                newUser = User(username=my_name + '-' + str(number), is_superuser=False, is_staff=False, is_active=True)
                if number==0:
                    newUser.username=my_name + "-" + SPIELLEITUNG_CODE
                newUser.set_password(str(int(hashlib.sha256(newUser.username.encode('utf-8')).hexdigest(), 16) % 10**4))
                newUser.save()
                my_group = Group.objects.get(name=KUNDEN)
                newUser.groups.add(my_group)

                if customer == 1:
                    newUser.groups.add(Group.objects.get(name=K1))
                if customer == 2:
                    newUser.groups.add(Group.objects.get(name=K2))
                if customer == 3:
                    newUser.groups.add(Group.objects.get(name=K3))
                if number==0:
                    newUser.groups.add(Group.objects.get(name=SPIELLEITUNG))
        

        #Kundendienst
        for number in range(0, PLAYER_AMOUNT_KUNDENDIENST + 1):
            my_name = KUNDENDIENST_CODE
            newUser = User(username=my_name + '-'  + str(number), is_superuser=False, is_staff=False, is_active=True)
            if number==0:
                    newUser.username=my_name + "-" + SPIELLEITUNG_CODE
            newUser.set_password(str(int(hashlib.sha256(newUser.username.encode('utf-8')).hexdigest(), 16) % 10**4))
            newUser.save()
            my_group = Group.objects.get(name=KUNDENDIENST)
            newUser.groups.add(my_group)
            my_group = Group.objects.get(name=JOGA)
            newUser.groups.add(my_group)
            if number==0:
                newUser.groups.add(Group.objects.get(name=SPIELLEITUNG))

        #Interne Dienstleistung
        for number in range(0, PLAYER_AMOUNT_INTERNE_DIENSTLEISTUNG + 1):
            my_name = INTERNE_DIENSTLEISTUNG_CODE
            newUser = User(username=my_name + '-'  + str(number), is_superuser=False, is_staff=False, is_active=True)
            if number==0:
                newUser.username=my_name + "-" + SPIELLEITUNG_CODE
            newUser.set_password(str(int(hashlib.sha256(newUser.username.encode('utf-8')).hexdigest(), 16) % 10**4))
            newUser.save()
            my_group = Group.objects.get(name=INTERNE_DIENSTLEISTUNG)
            newUser.groups.add(my_group)
            my_group = Group.objects.get(name=JOGA)
            newUser.groups.add(my_group)
            if number==0:
                newUser.groups.add(Group.objects.get(name=SPIELLEITUNG))

        #Produktionsdienstleistung
        for number in range(0, PLAYER_AMOUNT_PRODUKTIONSDIENSTLEISTUNG + 1):
            my_name = PRODUKTIONSDIENSTLEISTUNG_CODE
            newUser = User(username=my_name + '-'  + str(number), is_superuser=False, is_staff=False, is_active=True)
            if number==0:
                newUser.username=my_name + "-" + SPIELLEITUNG_CODE
            newUser.set_password(str(int(hashlib.sha256(newUser.username.encode('utf-8')).hexdigest(), 16) % 10**4))
            newUser.save()
            my_group = Group.objects.get(name=PRODUKTIONSDIENSTLEISTUNG)
            newUser.groups.add(my_group)
            my_group = Group.objects.get(name=JOGA)
            newUser.groups.add(my_group)
            if number==0:
                newUser.groups.add(Group.objects.get(name=SPIELLEITUNG))

        #Produktion
        for number in range(0, PLAYER_AMOUNT_PRODUKTION + 1):
            my_name = PRODUKTION_CODE
            newUser = User(username=my_name + '-' + str(number), is_superuser=False, is_staff=False, is_active=True)
            if number==0:
                newUser.username= my_name + "-" + SPIELLEITUNG_CODE
            newUser.set_password(str(int(hashlib.sha256(newUser.username.encode('utf-8')).hexdigest(), 16) % 10**4))
            newUser.save()
            my_group = Group.objects.get(name=PRODUKTION)
            newUser.groups.add(my_group)
            my_group = Group.objects.get(name=JOGA)
            newUser.groups.add(my_group)
            if number==0:
                newUser.groups.add(Group.objects.get(name=SPIELLEITUNG))

        #Lieferanten
        for supplier in range(1, 4):
            for number in range(0, PLAYER_AMOUNT_LIEFERANTEN + 1):
                my_name = LIEFERANTEN_CODE + str(supplier)
                newUser = User(username=my_name + '-'  + str(number), is_superuser=False, is_staff=False, is_active=True)
                if number==0:
                    newUser.username=my_name + "-" + SPIELLEITUNG_CODE
                newUser.set_password(str(int(hashlib.sha256(newUser.username.encode('utf-8')).hexdigest(), 16) % 10**4))
                newUser.save()
                my_group = Group.objects.get(name=LIEFERANTEN)
                newUser.groups.add(my_group)

                if supplier == 1:
                    newUser.groups.add(Group.objects.get(name=L100))
                elif supplier == 2:
                    newUser.groups.add(Group.objects.get(name=L200))
                elif supplier == 3:
                    newUser.groups.add(Group.objects.get(name=L300))

                if number==0:
                    newUser.groups.add(Group.objects.get(name=SPIELLEITUNG))
        
        #Einstellungen
        LiveSettings.load()
        print("Livesettings initialisiert!")

    dependencies = [
        ('gtapp', '0001_initial'),  
    ]           
    
    operations = [
        migrations.RunPython(insert_permissions),
        migrations.RunPython(insert_usergroups),
    ]
    