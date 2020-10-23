#This is the migration file for all master data to initialize a new round of the game

from django.db import migrations
from django.contrib.auth.models import User, Group, Permission
from gtapp.constants import *
from gtapp.models import *

class Migration(migrations.Migration):
    atomic = False
        
    def insert_groups(apps, schema_editor):

        Group.objects.create(name=LEITUNGSTEAM)
        Group.objects.create(name=KUNDEN)
        Group.objects.create(name=KUNDENDIENST)
        Group.objects.create(name=INTERNE_DIENSTLEISTUNG)
        Group.objects.create(name=PRODUKTIONSDIENSTLEISTUNG)
        Group.objects.create(name=PRODUKTION)
        Group.objects.create(name=LIEFERANTEN)
        Group.objects.create(name=SPIELLEITUNG)

    def insert_users(apps, schema_editor):
        
        #Fetch groups from the database
        group_lt    = Group.objects.filter(name=LEITUNGSTEAM).first()
        group_k     = Group.objects.filter(name=KUNDEN).first()
        group_kd    = Group.objects.filter(name=KUNDENDIENST).first()
        group_idl   = Group.objects.filter(name=INTERNE_DIENSTLEISTUNG).first()
        group_pdl   = Group.objects.filter(name=PRODUKTIONSDIENSTLEISTUNG).first()
        group_pro   = Group.objects.filter(name=PRODUKTION).first()
        group_l     = Group.objects.filter(name=LIEFERANTEN).first()
        group_sl    = Group.objects.filter(name=SPIELLEITUNG).first()
    
        #Create the amount of users, that is defined in the constants.players
        #and map them to the correct groups.
        #Username and passwords are numbered and start with the group-abbreviation.
        #For example: The second player in the production group
        #will have username and password = PRO2

        #Management
        for number in range(1, PLAYER_AMOUNT_LEITUNGSTEAM + 1):
            newUser = User(username=LEITUNGSTEAM_CODE + str(number), password=LEITUNGSTEAM_CODE + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.save()
            newUser.groups.add(group_lt)
        
        #Costumers
        for number in range(1, PLAYER_AMOUNT_KUNDEN + 1):
            newUser = User(username=KUNDEN_CODE + str(number), password=KUNDEN_CODE + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.save()
            newUser.groups.add(group_k)

        #Costumer service
        for number in range(1, PLAYER_AMOUNT_KUNDENDIENST + 1):
            newUser = User(username=KUNDENDIENST_CODE + str(number), password=KUNDENDIENST_CODE + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.save()
            newUser.groups.add(group_kd)

        #Internal service
        for number in range(1, PLAYER_AMOUNT_INTERNE_DIENSTLEISTUNG + 1):
            newUser = User(username=INTERNE_DIENSTLEISTUNG_CODE + str(number), password=INTERNE_DIENSTLEISTUNG_CODE + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.save()
            newUser.groups.add(group_idl)

        #Production service
        for number in range(1, PLAYER_AMOUNT_PRODUKTIONSDIENSTLEISTUNG + 1):
            newUser = User(username=PRODUKTIONSDIENSTLEISTUNG_CODE + str(number), password=PRODUKTIONSDIENSTLEISTUNG_CODE + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.save()
            newUser.groups.add(group_pdl)

        #Production
        for number in range(1, PLAYER_AMOUNT_PRODUKTION + 1):
            newUser = User(username=PRODUKTION_CODE + str(number), password=PRODUKTION_CODE + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.save()
            newUser.groups.add(group_pro)

        #Suppliers
        for number in range(1, PLAYER_AMOUNT_LIEFERANTEN + 1):
            newUser = User(username=LIEFERANTEN_CODE + str(number), password=LIEFERANTEN_CODE + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.save()
            newUser.groups.add(group_l)

        #Game Master
        for number in range(1, PLAYER_AMOUNT_SPIELLEITUNG + 1):
            newUser = User(username=SPIELLEITUNG_CODE + str(number), password=SPIELLEITUNG_CODE + str(number), is_superuser=False, is_staff=True, is_active=True)
            newUser.save()
            newUser.groups.add(group_sl)
    
    def insert_customers(apps, schema_editor):
        
        defaultCustomerStatus = Status.objects.filter(status=CUSTOMER_ACTIVE,table='CUSTOMER').first()
        
        Customer.objects.create(status=defaultCustomerStatus,name='K100')
        Customer.objects.create(status=defaultCustomerStatus,name='K200')
        Customer.objects.create(status=defaultCustomerStatus,name='K300')

    def insert_suppliers(apps, schema_editor):
        
        defaultSupplierStatus = Status.objects.filter(status=SUPPLIER_ACTIVE,table='SUPPLIER').first()
        
        Supplier.objects.create(status=defaultSupplierStatus,name='L100')
        Supplier.objects.create(status=defaultSupplierStatus,name='L200')
        Supplier.objects.create(status=defaultSupplierStatus,name='L300')

    def insert_parts(apps, schema_editor):

        defaultPartStatus = Status.objects.filter(status=PART_ACTIVE,table='PART').first()
        supplier_L100 = Supplier.objects.filter(name='L100').first()
        supplier_L200 = Supplier.objects.filter(name='L200').first()
        supplier_L300 = Supplier.objects.filter(name='L300').first()    

        Part.objects.create(status=defaultPartStatus, supplier=supplier_L100, part_no='T1', description='Welle 80', pack_quantity=8, install_quantity=4, initial_stock=6)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L100, part_no='T2', description='Welle 130', pack_quantity=8, install_quantity=4, initial_stock=3)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L100, part_no='T3', description='Strebe 230', pack_quantity=8, install_quantity=4, initial_stock=5)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L100, part_no='T4', description='Strebe 280', pack_quantity=8, install_quantity=4, initial_stock=2)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L100, part_no='T5', description='Rad', pack_quantity=13, install_quantity=4, initial_stock=3)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L200, part_no='T6', description='Hülse Hubelement', pack_quantity=10, install_quantity=2, initial_stock=0)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L200, part_no='T7', description='Wellenhülse', pack_quantity=12, install_quantity=8, initial_stock=2)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L200, part_no='T8', description='Schraube M5 X 20', pack_quantity=33, install_quantity=12, initial_stock=6)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L200, part_no='T9', description='Schraube M6 + Scheibe', pack_quantity=16, install_quantity=2, initial_stock=2)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L300, part_no='T10', description='Träger Fahrgestell', pack_quantity=5, install_quantity=2, initial_stock=1)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L300, part_no='T11', description='Träger Lastmodul', pack_quantity=5, install_quantity=2, initial_stock=0)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L300, part_no='T12', description='Querstrebe 120', pack_quantity=8, install_quantity=4, initial_stock=2)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L300, part_no='T13', description='Querstrebe 170', pack_quantity=6, install_quantity=4, initial_stock=2)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L300, part_no='T14', description='Sicherungsblech', pack_quantity=8, install_quantity=2, initial_stock=1)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L300, part_no='T15', description='Schraube M5 X 8', pack_quantity=8, install_quantity=6, initial_stock=0)

    def insert_stocks(apps, schema_editor):

        #Iterate through all entries in the parts-table
        for part_no in range(1, Part.objects.count() + 1):

            #Fetch part according to the current part_no
            currentPart         = Part.objects.filter(part_no='T' + str(part_no)).first()
            #Create stock-entry for the current part and initialize the stock according to the parts attribute initial_stock
            Stock.objects.create(part=currentPart, stock=currentPart.initial_stock)


    def insert_articles(apps, schema_editor):
       
        defaultArticleStatus = Status.objects.filter(status=ARTICLE_ACTIVE,table='ARTICLE').first()
                  
        mobStandard150  = Article(status=defaultArticleStatus,article_no=1, description='Mob Standard 150')
        mobStandard200  = Article(status=defaultArticleStatus,article_no=2, description='Mob Standard 200')
        mobHigh150      = Article(status=defaultArticleStatus,article_no=3, description='High Mob 150')
        mobHigh200      = Article(status=defaultArticleStatus,article_no=4, description='High Mob 200')

        mobStandard150.save()
        mobStandard200.save()
        mobHigh150.save()
        mobHigh200.save()

        #Iterate through all entries in the parts-table
        for part_no in range(1, Part.objects.count() + 1):

            #Fetch part according to the current part_no
            currentPart         = Part.objects.filter(part_no='T' + str(part_no)).first()
            
            #Most parts are used for all articles. Individual articles can be easier distinguished by the parts they lack
            if currentPart.part_no not in ['T2', 'T4', 'T13']:
                mobStandard150.parts.add(currentPart,through_defaults={'quantity':currentPart.install_quantity})

            if currentPart.part_no not in ['T1', 'T4', 'T12']:
                mobStandard200.parts.add(currentPart,through_defaults={'quantity':currentPart.install_quantity})

            if currentPart.part_no not in ['T2', 'T3', 'T13']:
                mobHigh150.parts.add(currentPart,through_defaults={'quantity':currentPart.install_quantity})                

            if currentPart.part_no not in ['T1', 'T3', 'T12']:
                mobHigh200.parts.add(currentPart,through_defaults={'quantity':currentPart.install_quantity})          


    dependencies = [
        ('gtapp', '0001_initial'),
        ('gtapp', '0002_insert_statuses'),
    ]

    operations = [
        migrations.RunPython(insert_groups),
        migrations.RunPython(insert_users),
        migrations.RunPython(insert_customers),
        migrations.RunPython(insert_suppliers),
        migrations.RunPython(insert_parts),
        migrations.RunPython(insert_stocks),
        migrations.RunPython(insert_articles),
    ]