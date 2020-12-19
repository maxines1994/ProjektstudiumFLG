"""
Diese Migrations-Datei fuegt alle Stammdaten hinzu.
"""

from django.db import migrations
from django.contrib.auth.models import User, Group, Permission
from gtapp.constants import *
from gtapp.models import *

class Migration(migrations.Migration):
    atomic = False
        
    def insert_customers(apps, schema_editor):
        
        defaultCustomerStatus = Status.objects.get(code=CUSTOMER_ACTIVE,table='CUSTOMER')
        
        Customer.objects.create(status=defaultCustomerStatus,name='K100')
        Customer.objects.create(status=defaultCustomerStatus,name='K200')
        Customer.objects.create(status=defaultCustomerStatus,name='K300')

    def insert_suppliers(apps, schema_editor):
        
        defaultSupplierStatus = Status.objects.get(code=SUPPLIER_ACTIVE,table='SUPPLIER')
        
        Supplier.objects.create(status=defaultSupplierStatus,name='L100')
        Supplier.objects.create(status=defaultSupplierStatus,name='L200')
        Supplier.objects.create(status=defaultSupplierStatus,name='L300')

    def insert_parts(apps, schema_editor):

        defaultPartStatus = Status.objects.get(code=PART_ACTIVE,table='PART')
        supplier_L100 = Supplier.objects.get(name='L100')
        supplier_L200 = Supplier.objects.get(name='L200')
        supplier_L300 = Supplier.objects.get(name='L300')    

        Part.objects.create(status=defaultPartStatus, supplier=supplier_L100, part_no='T1', description='Welle 80', pack_quantity=8, install_quantity=4, initial_stock=6, total_stock=50)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L100, part_no='T2', description='Welle 130', pack_quantity=8, install_quantity=4, initial_stock=3, total_stock=50)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L100, part_no='T3', description='Strebe 230', pack_quantity=8, install_quantity=4, initial_stock=5, total_stock=40)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L100, part_no='T4', description='Strebe 280', pack_quantity=8, install_quantity=4, initial_stock=2, total_stock=40)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L100, part_no='T5', description='Rad', pack_quantity=13, install_quantity=4, initial_stock=3, total_stock=80)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L200, part_no='T6', description='Hülse Hubelement', pack_quantity=10, install_quantity=2, initial_stock=0, total_stock=50)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L200, part_no='T7', description='Wellenhülse', pack_quantity=12, install_quantity=8, initial_stock=2, total_stock=60)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L200, part_no='T8', description='Schraube M5 X 20', pack_quantity=33, install_quantity=12, initial_stock=6, total_stock=200)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L200, part_no='T9', description='Schraube M6 + Scheibe', pack_quantity=16, install_quantity=2, initial_stock=2, total_stock=100)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L300, part_no='T10', description='Träger Fahrgestell', pack_quantity=5, install_quantity=2, initial_stock=1, total_stock=40)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L300, part_no='T11', description='Träger Lastmodul', pack_quantity=5, install_quantity=2, initial_stock=0, total_stock=40)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L300, part_no='T12', description='Querstrebe 120', pack_quantity=8, install_quantity=4, initial_stock=2, total_stock=40)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L300, part_no='T13', description='Querstrebe 170', pack_quantity=6, install_quantity=4, initial_stock=2, total_stock=40)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L300, part_no='T14', description='Sicherungsblech', pack_quantity=8, install_quantity=2, initial_stock=1, total_stock=40)
        Part.objects.create(status=defaultPartStatus, supplier=supplier_L300, part_no='T15', description='Schraube M5 X 8', pack_quantity=8, install_quantity=6, initial_stock=0, total_stock=40)

    def insert_stocks(apps, schema_editor):

        #Durchlaufe alle Eintraege in der Parts-Tabelle
        for part_no in range(1, Part.objects.count() + 1):
            
            #Schnapp dir ein Teil entsprechend der aktuellen Teilenummer
            currentPart = Part.objects.get(part_no='T' + str(part_no))

            #Erstelle einen Bestands-Datensatz fuer das aktuelle Teil und initialisiere den Bestand entsprechend des beim Teil hinterlegten initial_stock
            Stock.objects.create(part=currentPart, stock=currentPart.initial_stock, is_supplier_stock=False)

            #Erstelle nun einen Bestands-Datensatz fuer den Lieferanten anhand Differenz des beim Teil hinterlegten total_amount und dem initial_stock
            Stock.objects.create(part=currentPart, stock=currentPart.total_stock - currentPart.initial_stock, is_supplier_stock=True)


    def insert_articles(apps, schema_editor):
       
        defaultArticleStatus = Status.objects.get(code=ARTICLE_ACTIVE,table='ARTICLE')
                  
        mobStandard150  = Article(status=defaultArticleStatus,article_no=1, description='Mob Standard 150')
        mobStandard200  = Article(status=defaultArticleStatus,article_no=2, description='Mob Standard 200')
        mobHigh150      = Article(status=defaultArticleStatus,article_no=3, description='High Mob 150')
        mobHigh200      = Article(status=defaultArticleStatus,article_no=4, description='High Mob 200')

        mobStandard150.save()
        mobStandard200.save()
        mobHigh150.save()
        mobHigh200.save()

        #Durchlaufe alle Eintraege in der Parts-Tabelle
        for part_no in range(1, Part.objects.count() + 1):

            #Schnapp dir ein Teil entsprechend der aktuellen Teilenummer
            currentPart         = Part.objects.filter(part_no='T' + str(part_no)).first()
            
            #Die meisten Teile werden fuer alle Artikel verwendet. Einzelne Artikel lassen sich also leichter durch die Teile unterscheiden, die ihnen fehlen.
            #Hinterlege das Teil mit der install_quantity bei allen Artikeln, die das aktuelle Teil verwenden. Dies geschieht durch die Tabelle ArtiParts.
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
        ('gtapp', '0002_insert_translations'),
        ('gtapp', '0003_insert_usergroups'),
        ('gtapp', '0005_insert_unknowns'),
        ('gtapp', '0004_insert_statuses'),
    ]

    operations = [
        migrations.RunPython(insert_customers),
        migrations.RunPython(insert_suppliers),
        migrations.RunPython(insert_parts),
        migrations.RunPython(insert_stocks),
        migrations.RunPython(insert_articles),
    ]