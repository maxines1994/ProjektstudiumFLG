"""
Diese Migrations-Datei fuegt alle Stammdaten hinzu.
"""

from django.db import migrations
from django.contrib.auth.models import User, Group, Permission
from gtapp.constants import *
from gtapp.models import *
from gtapp.models.productionsteps import ProductionSteps

class Migration(migrations.Migration):
    atomic = False
        
    def insert_customers(apps, schema_editor):
                
        Customer.objects.create(name=K1)
        Customer.objects.create(name=K2)
        Customer.objects.create(name=K3)

    def insert_suppliers(apps, schema_editor):
        
        Supplier.objects.create(name=L100)
        Supplier.objects.create(name=L200)
        Supplier.objects.create(name=L300)

    def insert_parts(apps, schema_editor):

        supplier_L100 = Supplier.objects.get(name=L100)
        supplier_L200 = Supplier.objects.get(name=L200)
        supplier_L300 = Supplier.objects.get(name=L300)  

        Part.objects.create(supplier=supplier_L100, part_no='T1', description='Welle 80', pack_quantity=8, install_quantity=4, initial_stock=6, total_stock=50, image='img/parts/07.png')
        Part.objects.create(supplier=supplier_L100, part_no='T2', description='Welle 130', pack_quantity=8, install_quantity=4, initial_stock=3, total_stock=50, image='img/parts/07.png') 
        Part.objects.create(supplier=supplier_L100, part_no='T3', description='Strebe 230', pack_quantity=8, install_quantity=4, initial_stock=5, total_stock=40, image='img/parts/06.png')
        Part.objects.create(supplier=supplier_L100, part_no='T4', description='Strebe 280', pack_quantity=8, install_quantity=4, initial_stock=2, total_stock=40, image='img/parts/06.png')
        Part.objects.create(supplier=supplier_L100, part_no='T5', description='Rad', pack_quantity=13, install_quantity=4, initial_stock=3, total_stock=80, image='img/parts/05.png')
        Part.objects.create(supplier=supplier_L200, part_no='T6', description='Hülse Hubelement', pack_quantity=10, install_quantity=2, initial_stock=0, total_stock=50, image='img/parts/08.png')
        Part.objects.create(supplier=supplier_L200, part_no='T7', description='Wellenhülse', pack_quantity=12, install_quantity=8, initial_stock=2, total_stock=60, image='img/parts/09.png')
        Part.objects.create(supplier=supplier_L200, part_no='T8', description='Schraube M5 X 20', pack_quantity=33, install_quantity=12, initial_stock=6, total_stock=200, image='img/parts/10.png')
        Part.objects.create(supplier=supplier_L200, part_no='T9', description='Schraube M6 + Scheibe', pack_quantity=16, install_quantity=2, initial_stock=2, total_stock=100, image='img/parts/12.png')
        Part.objects.create(supplier=supplier_L300, part_no='T10', description='Träger Fahrgestell', pack_quantity=5, install_quantity=2, initial_stock=1, total_stock=40, image='img/parts/01.png')
        Part.objects.create(supplier=supplier_L300, part_no='T11', description='Träger Lastmodul', pack_quantity=5, install_quantity=2, initial_stock=0, total_stock=40, image='img/parts/02.png')
        Part.objects.create(supplier=supplier_L300, part_no='T12', description='Querstrebe 120', pack_quantity=8, install_quantity=4, initial_stock=2, total_stock=40, image='img/parts/03.png')
        Part.objects.create(supplier=supplier_L300, part_no='T13', description='Querstrebe 170', pack_quantity=6, install_quantity=4, initial_stock=2, total_stock=40, image='img/parts/03.png')
        Part.objects.create(supplier=supplier_L300, part_no='T14', description='Sicherungsblech', pack_quantity=8, install_quantity=2, initial_stock=1, total_stock=40, image='img/parts/04.png')
        Part.objects.create(supplier=supplier_L300, part_no='T15', description='Schraube M5 X 8', pack_quantity=8, install_quantity=6, initial_stock=0, total_stock=40, image='img/parts/11.png')

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
                         
        mobStandard150  = Article(article_no=1, description='Mob Standard 150')
        mobStandard200  = Article(article_no=2, description='Mob Standard 200')
        mobHigh150      = Article(article_no=3, description='High Mob 150')
        mobHigh200      = Article(article_no=4, description='High Mob 200')

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
                mobStandard150.parts.add(currentPart, through_defaults={'quantity':currentPart.install_quantity})

            if currentPart.part_no not in ['T1', 'T4', 'T12']:
                mobStandard200.parts.add(currentPart, through_defaults={'quantity':currentPart.install_quantity})

            if currentPart.part_no not in ['T2', 'T3', 'T13']:
                mobHigh150.parts.add(currentPart, through_defaults={'quantity':currentPart.install_quantity})                

            if currentPart.part_no not in ['T1', 'T3', 'T12']:
                mobHigh200.parts.add(currentPart, through_defaults={'quantity':currentPart.install_quantity})          


    def insert_productionsteps(apps, schema_editor):

        steps = []
        #Datenbankwerte für die Produktionsschritte von M1 
        step_m1_s1_1 = ProductionSteps(production_step=1, quantity=2, article_id=1, part_id=6)
        steps.append(step_m1_s1_1)

        step_m1_s1_2 = ProductionSteps(production_step=1, quantity=2, article_id=1, part_id=9)
        steps.append(step_m1_s1_2)
        
        step_m1_s1_3 = ProductionSteps(production_step=1, quantity=4, article_id=1, part_id=3)
        steps.append(step_m1_s1_3)

        step_m1_s2_1 = ProductionSteps(production_step=2, quantity=2, article_id=1, part_id=10)
        steps.append(step_m1_s2_1)

        step_m1_s2_2 = ProductionSteps(production_step=2, quantity=2, article_id=1, part_id=12)
        steps.append(step_m1_s2_2)

        step_m1_s2_3 = ProductionSteps(production_step=2, quantity=4, article_id=1, part_id=8)
        steps.append(step_m1_s2_3)

        step_m1_s3_1 = ProductionSteps(production_step=3, quantity=2, article_id=1, part_id=12)
        steps.append(step_m1_s3_1)

        step_m1_s3_2 = ProductionSteps(production_step=3, quantity=1, article_id=1, part_id=11)
        steps.append(step_m1_s3_2)

        step_m1_s3_3 = ProductionSteps(production_step=3, quantity=2, article_id=1, part_id=8)
        steps.append(step_m1_s3_3)

        step_m1_s4_1 = ProductionSteps(production_step=4, quantity=4, article_id=1, part_id=1)
        steps.append(step_m1_s4_1)

        step_m1_s4_2 = ProductionSteps(production_step=4, quantity=4, article_id=1, part_id=7)
        steps.append(step_m1_s4_2)

        step_m1_s5_1 = ProductionSteps(production_step=5, quantity=4, article_id=1, part_id=7)
        steps.append(step_m1_s5_1)

        step_m1_s6_1 = ProductionSteps(production_step=6, quantity=1, article_id=1, part_id=11)
        steps.append(step_m1_s6_1)

        step_m1_s6_2 = ProductionSteps(production_step=6, quantity=2, article_id=1, part_id=8)
        steps.append(step_m1_s6_2)

        step_m1_s7_1 = ProductionSteps(production_step=7, quantity=2, article_id=1, part_id=14)
        steps.append(step_m1_s7_1)

        step_m1_s7_2 = ProductionSteps(production_step=7, quantity=6, article_id=1, part_id=15)
        steps.append(step_m1_s7_2)

        step_m1_s8_1 = ProductionSteps(production_step=8, quantity=4, article_id=1, part_id=5)
        steps.append(step_m1_s8_1)

        step_m1_s8_2 = ProductionSteps(production_step=8, quantity=4, article_id=1, part_id=15)
        steps.append(step_m1_s8_2)


        #Datenbankwerte für die Produktionsschritte von M2
        step_m2_s1_1 = ProductionSteps(production_step=1, quantity=2, article_id=2, part_id=6)
        steps.append(step_m2_s1_1)

        step_m2_s1_2 = ProductionSteps(production_step=1, quantity=2, article_id=2, part_id=9)
        steps.append(step_m2_s1_2)
        
        step_m2_s1_3 = ProductionSteps(production_step=1, quantity=4, article_id=2, part_id=3)
        steps.append(step_m2_s1_3)

        step_m2_s2_1 = ProductionSteps(production_step=2, quantity=2, article_id=2, part_id=10)
        steps.append(step_m2_s2_1)

        step_m2_s2_2 = ProductionSteps(production_step=2, quantity=2, article_id=2, part_id=13)
        steps.append(step_m2_s2_2)

        step_m2_s2_3 = ProductionSteps(production_step=2, quantity=4, article_id=2, part_id=8)
        steps.append(step_m2_s2_3)

        step_m2_s3_1 = ProductionSteps(production_step=3, quantity=2, article_id=2, part_id=13)
        steps.append(step_m2_s3_1)

        step_m2_s3_2 = ProductionSteps(production_step=3, quantity=1, article_id=2, part_id=11)
        steps.append(step_m2_s3_2)

        step_m2_s3_3 = ProductionSteps(production_step=3, quantity=2, article_id=2, part_id=8)
        steps.append(step_m2_s3_3)

        step_m2_s4_1 = ProductionSteps(production_step=4, quantity=4, article_id=2, part_id=2)
        steps.append(step_m2_s4_1)

        step_m2_s4_2 = ProductionSteps(production_step=4, quantity=4, article_id=2, part_id=7)
        steps.append(step_m2_s4_2)

        step_m2_s5_1 = ProductionSteps(production_step=5, quantity=4, article_id=2, part_id=7)
        steps.append(step_m2_s5_1)

        step_m2_s6_1 = ProductionSteps(production_step=6, quantity=1, article_id=2, part_id=11)
        steps.append(step_m2_s6_1)

        step_m2_s6_2 = ProductionSteps(production_step=6, quantity=2, article_id=2, part_id=8)
        steps.append(step_m2_s6_2)

        step_m2_s7_1 = ProductionSteps(production_step=7, quantity=2, article_id=2, part_id=14)
        steps.append(step_m2_s7_1)

        step_m2_s7_2 = ProductionSteps(production_step=7, quantity=6, article_id=2, part_id=15)
        steps.append(step_m2_s7_2)

        step_m2_s8_1 = ProductionSteps(production_step=8, quantity=4, article_id=2, part_id=5)
        steps.append(step_m2_s8_1)

        step_m2_s8_2 = ProductionSteps(production_step=8, quantity=4, article_id=2, part_id=15)
        steps.append(step_m2_s8_2)


        #Datenbankwerte für die Produktionsschritte von M3
        step_m3_s1_1 = ProductionSteps(production_step=1, quantity=2, article_id=3, part_id=6)
        steps.append(step_m3_s1_1)

        step_m3_s1_2 = ProductionSteps(production_step=1, quantity=2, article_id=3, part_id=9)
        steps.append(step_m3_s1_2)
        
        step_m3_s1_3 = ProductionSteps(production_step=1, quantity=4, article_id=3, part_id=4)
        steps.append(step_m3_s1_3)

        step_m3_s2_1 = ProductionSteps(production_step=2, quantity=2, article_id=3, part_id=10)
        steps.append(step_m3_s2_1)

        step_m3_s2_2 = ProductionSteps(production_step=2, quantity=2, article_id=3, part_id=12)
        steps.append(step_m3_s2_2)

        step_m3_s2_3 = ProductionSteps(production_step=2, quantity=4, article_id=3, part_id=8)
        steps.append(step_m3_s2_3)

        step_m3_s3_1 = ProductionSteps(production_step=3, quantity=2, article_id=3, part_id=12)
        steps.append(step_m3_s3_1)

        step_m3_s3_2 = ProductionSteps(production_step=3, quantity=1, article_id=3, part_id=11)
        steps.append(step_m3_s3_2)

        step_m3_s3_3 = ProductionSteps(production_step=3, quantity=2, article_id=3, part_id=8)
        steps.append(step_m3_s3_3)

        step_m3_s4_1 = ProductionSteps(production_step=4, quantity=4, article_id=3, part_id=1)
        steps.append(step_m3_s4_1)

        step_m3_s4_2 = ProductionSteps(production_step=4, quantity=4, article_id=3, part_id=7)
        steps.append(step_m3_s4_2)

        step_m3_s5_1 = ProductionSteps(production_step=5, quantity=4, article_id=3, part_id=7)
        steps.append(step_m3_s5_1)

        step_m3_s6_1 = ProductionSteps(production_step=6, quantity=1, article_id=3, part_id=11)
        steps.append(step_m3_s6_1)

        step_m3_s6_2 = ProductionSteps(production_step=6, quantity=2, article_id=3, part_id=8)
        steps.append(step_m3_s6_2)

        step_m3_s7_1 = ProductionSteps(production_step=7, quantity=2, article_id=3, part_id=14)
        steps.append(step_m3_s7_1)

        step_m3_s7_2 = ProductionSteps(production_step=7, quantity=6, article_id=3, part_id=15)
        steps.append(step_m3_s7_2)

        step_m3_s8_1 = ProductionSteps(production_step=8, quantity=4, article_id=3, part_id=5)
        steps.append(step_m3_s8_1)

        step_m3_s8_2 = ProductionSteps(production_step=8, quantity=4, article_id=3, part_id=15)
        steps.append(step_m3_s8_2)


        #Datenbankwerte für die Produktionsschritte von M4
        step_m4_s1_1 = ProductionSteps(production_step=1, quantity=2, article_id=4, part_id=6)
        steps.append(step_m4_s1_1)

        step_m4_s1_2 = ProductionSteps(production_step=1, quantity=2, article_id=4, part_id=9)
        steps.append(step_m4_s1_2)
        
        step_m4_s1_3 = ProductionSteps(production_step=1, quantity=4, article_id=4, part_id=4)
        steps.append(step_m4_s1_3)

        step_m4_s2_1 = ProductionSteps(production_step=2, quantity=2, article_id=4, part_id=10)
        steps.append(step_m4_s2_1)

        step_m4_s2_2 = ProductionSteps(production_step=2, quantity=2, article_id=4, part_id=13)
        steps.append(step_m4_s2_2)

        step_m4_s2_3 = ProductionSteps(production_step=2, quantity=4, article_id=4, part_id=8)
        steps.append(step_m4_s2_3)

        step_m4_s3_1 = ProductionSteps(production_step=3, quantity=2, article_id=4, part_id=13)
        steps.append(step_m4_s3_1)

        step_m4_s3_2 = ProductionSteps(production_step=3, quantity=1, article_id=4, part_id=11)
        steps.append(step_m4_s3_2)

        step_m4_s3_3 = ProductionSteps(production_step=3, quantity=2, article_id=4, part_id=8)
        steps.append(step_m4_s3_3)

        step_m4_s4_1 = ProductionSteps(production_step=4, quantity=4, article_id=4, part_id=2)
        steps.append(step_m4_s4_1)

        step_m4_s4_2 = ProductionSteps(production_step=4, quantity=4, article_id=4, part_id=7)
        steps.append(step_m4_s4_2)

        step_m4_s5_1 = ProductionSteps(production_step=5, quantity=4, article_id=4, part_id=7)
        steps.append(step_m4_s5_1)

        step_m4_s6_1 = ProductionSteps(production_step=6, quantity=1, article_id=4, part_id=11)
        steps.append(step_m4_s6_1)

        step_m4_s6_2 = ProductionSteps(production_step=6, quantity=2, article_id=4, part_id=8)
        steps.append(step_m4_s6_2)

        step_m4_s7_1 = ProductionSteps(production_step=7, quantity=2, article_id=4, part_id=14)
        steps.append(step_m4_s7_1)

        step_m4_s7_2 = ProductionSteps(production_step=7, quantity=6, article_id=4, part_id=15)
        steps.append(step_m4_s7_2)

        step_m4_s8_1 = ProductionSteps(production_step=8, quantity=4, article_id=4, part_id=5)
        steps.append(step_m4_s8_1)

        step_m4_s8_2 = ProductionSteps(production_step=8, quantity=4, article_id=4, part_id=15)
        steps.append(step_m4_s8_2)

        for step in steps:
            step.save()
        
    def insert_bookingcodes(apps, schema_editor):
        for item in dir(bookingcodes):
            if not item.startswith("__"):              
                itemBookingcode = str(getattr(bookingcodes, item))               
                itemDescription = str(item.split('_', 1)[1].replace('_', ' ').casefold().title())
                BookingCode.objects.create(code=itemBookingcode, description=itemDescription)

    def insert_tasktypes(apps, schema_editor):

        #

        #JOGA
        TaskType.objects.create(id=1    , title = "Auftrag freigeben"                           , description ="Bitte geben Sie den Auftrag frei!"                                                                                                                          , status_model = CustOrder.__name__         , task_model= CustOrder.__name__        , status=CustOrder.Status.ERFASST                               , view_url = 'cust_order_alter'        , view_kwargs_id = 'cust_order_id'      , group=Group.objects.get(name=KUNDENDIENST))
        TaskType.objects.create(id=2    , title = "Bestand prüfen"                              , description ="Bitte prüfen Sie den Bestand"                                                                                                                               , status_model = CustOrderDet.__name__      , task_model= CustOrderDet.__name__     , status=CustOrderDet.Status.BESTANDSPRUEFUNG_AUSSTEHEND        , view_url = 'manufacturing_list'      , view_kwargs_id = ''                   , group=Group.objects.get(name=PRODUKTIONSDIENSTLEISTUNG)   , for_all_details=True)
        TaskType.objects.create(id=3    , title = "Bestellung erstellen"                        , description ="Bitte bestellen Sie die nicht vorrätigen Teile bei dem Lieferanten 300!"                                                                                    , status_model = CustOrderDet.__name__      , task_model= SuppOrder.__name__        , status=UNKNOWN                                                , view_url = 'supp_order'              , view_kwargs_id = ''                   , group=Group.objects.get(name=PRODUKTIONSDIENSTLEISTUNG))
        TaskType.objects.create(id=4    , title = "Wareneingang"                                , description ="Bitte führen Sie den Wareingang durch und prüfen Sie dabei die eingetroffenen Teile."                                                                       , status_model = SuppOrder.__name__         , task_model= SuppOrder.__name__        , status=SuppOrder.Status.GELIEFERT                             , view_url = 'supp_order_alter'        , view_kwargs_id = 'supp_order_id'      , group=Group.objects.get(name=PRODUKTIONSDIENSTLEISTUNG))
        TaskType.objects.create(id=5    , title = "Teilelieferung an Produktion"                , description ="Bitte liefern Sie die Teile an die Produktion!"                                                                                                             , status_model = CustOrderDet.__name__      , task_model= CustOrderDet.__name__     , status=UNKNOWN                                                , view_url = 'manufacturing_list'      , view_kwargs_id = ''                   , group=Group.objects.get(name=PRODUKTIONSDIENSTLEISTUNG))
        TaskType.objects.create(id=6    , title = "Hebebühne produzieren"                       , description ="Bitte bauen Sie die Hebebühne nach der Anleitung und führen Sie am Ende eine Qualitätsprüfung durch."                                                       , status_model = CustOrderDet.__name__      , task_model= CustOrderDet.__name__     , status=CustOrderDet.Status.IN_PRODUKTION                      , view_url = 'manufacturing_list'      , view_kwargs_id = ''                   , group=Group.objects.get(name=PRODUKTION))
        TaskType.objects.create(id=7    , title = "Hebebühne an Kundendienst leifern"           , description ="Bitte liefern Sie die Hebebühne an den Kundendienst"                                                                                                        , status_model = CustOrderDet.__name__      , task_model= CustOrderDet.__name__     , status=CustOrderDet.Status.LIEFERUNG_AN_KD_AUSSTEHEND         , view_url = 'manufacturing_list'      , view_kwargs_id = ''                   , group=Group.objects.get(name=PRODUKTION))
        TaskType.objects.create(id=8    , title = "Hebebühne an Kunden leifern"                 , description ="Bitte liefern Sie die Hebebühne an den Kunden"                                                                                                              , status_model = CustOrderDet.__name__      , task_model= CustOrderDet.__name__     , status=CustOrderDet.Status.LIEFERUNG_AN_K_AUSSTEHEND          , view_url = 'cust_order_alter'        , view_kwargs_id = 'cust_order_id'      , group=Group.objects.get(name=KUNDENDIENST))

        #Lieferant 300  
        TaskType.objects.create(id=9    , title = "Bestand prüfen"                              , description ="Bitte prüfen Sie den Bestand!"                                                                                                                              , status_model = SuppOrder.__name__         , task_model= SuppOrder.__name__        , status=SuppOrder.Status.BESTANDSPRUEFUNG_AUSSTEHEND           , view_url = 'supp_order_alter'        , view_kwargs_id = 'supp_order_id'      , group=Group.objects.get(name=L300))
        TaskType.objects.create(id=10   , title = "Lieferung versenden"                         , description ="Bitte stellen Sie die Box mit den bestellten Teilen fertg und senden Sie diese an JOGA. Denken Sie daran eine E-Mail mit der Box-Nummer an JOGA zu senden." , status_model = SuppOrder.__name__         , task_model= SuppOrder.__name__        , status=SuppOrder.Status.LIEFERUNG_AN_JOGA_AUSSTEHEND          , view_url = 'supp_order_alter'        , view_kwargs_id = 'supp_order_id'      , group=Group.objects.get(name=L300))

        #Bestellung Kunde 1, 2, 3, Joga 
        TaskType.objects.create(id=11   , title = "Wareneingang buchen"                         , description ="Bitte buchen Sie den Wareneingang und führen Sie gleichzeitig eine Qualitätsprüfung durch."                                                                 , status_model = CustOrderDet.__name__      , task_model= CustOrderDet.__name__     , status=CustOrderDet.Status.GELIEFERT                          , view_url = 'cust_order_alter'        , view_kwargs_id = 'cust_order_id'      , group=Group.objects.get(name=K1))
        TaskType.objects.create(id=12   , title = "Wareneingang buchen"                         , description ="Bitte buchen Sie den Wareneingang und führen Sie gleichzeitig eine Qualitätsprüfung durch."                                                                 , status_model = CustOrderDet.__name__      , task_model= CustOrderDet.__name__     , status=CustOrderDet.Status.GELIEFERT                          , view_url = 'cust_order_alter'        , view_kwargs_id = 'cust_order_id'      , group=Group.objects.get(name=K2))
        TaskType.objects.create(id=13   , title = "Wareneingang buchen"                         , description ="Bitte buchen Sie den Wareneingang und führen Sie gleichzeitig eine Qualitätsprüfung durch."                                                                 , status_model = CustOrderDet.__name__      , task_model= CustOrderDet.__name__     , status=CustOrderDet.Status.GELIEFERT                          , view_url = 'cust_order_alter'        , view_kwargs_id = 'cust_order_id'      , group=Group.objects.get(name=K3))
        TaskType.objects.create(id=14   , title = "Wareneingang buchen"                         , description ="Bitte buchen Sie den Wareneingang und führen Sie gleichzeitig eine Qualitätsprüfung durch."                                                                 , status_model = SuppOrder.__name__         , task_model= SuppOrder.__name__        , status=SuppOrder.Status.GELIEFERT                             , view_url = 'supp_order_alter'        , view_kwargs_id = 'supp_order_id'      , group=Group.objects.get(name=PRODUKTIONSDIENSTLEISTUNG))

        #weitere von JOGA   
        TaskType.objects.create(id=15   , title = "Bestellung freigeben"                        , description ="Bitte geben Sie die Bestellung frei"                                                                                                                        , status_model = SuppOrder.__name__         , task_model= SuppOrder.__name__        , status=SuppOrder.Status.ERFASST                               , view_url = 'supp_order_alter'        , view_kwargs_id = 'supp_order_id'      , group=Group.objects.get(name=PRODUKTIONSDIENSTLEISTUNG))
        #Bestellung freigeben Kunden (Kunde 1, 2, 3, PDL)                           
        TaskType.objects.create(id=16   , title = "Bestellung freigeben"                        , description ="Bitte geben Sie die Bestellung frei"                                                                                                                        , status_model = CustOrderDet.__name__      , task_model= CustOrderDet.__name__     , status=CustOrderDet.Status.ERFASST                            , view_url = 'cust_order_alter'        , view_kwargs_id = 'cust_order_id'      , group=Group.objects.get(name=K1))
        TaskType.objects.create(id=17   , title = "Bestellung freigeben"                        , description ="Bitte geben Sie die Bestellung frei"                                                                                                                        , status_model = CustOrderDet.__name__      , task_model= CustOrderDet.__name__     , status=CustOrderDet.Status.ERFASST                            , view_url = 'cust_order_alter'        , view_kwargs_id = 'cust_order_id'      , group=Group.objects.get(name=K2))
        TaskType.objects.create(id=18   , title = "Bestellung freigeben"                        , description ="Bitte geben Sie die Bestellung frei"                                                                                                                        , status_model = CustOrderDet.__name__      , task_model= CustOrderDet.__name__     , status=CustOrderDet.Status.ERFASST                            , view_url = 'cust_order_alter'        , view_kwargs_id = 'cust_order_id'      , group=Group.objects.get(name=K3))
        TaskType.objects.create(id=19   , title = "Bestellung freigeben"                        , description ="Bitte geben Sie die Bestellung frei"                                                                                                                        , status_model = SuppOrder.__name__         , task_model= SuppOrder.__name__        , status=SuppOrder.Status.ERFASST                               , view_url = 'supp_order_alter'        , view_kwargs_id = 'supp_order_id'      , group=Group.objects.get(name=PRODUKTIONSDIENSTLEISTUNG))


        #Lieferant 300  
        TaskType.objects.create(id=20   , title = "Auftrag freigeben"                           , description ="Bitte geben Sie den Auftrag frei."                                                                                                                          , status_model = SuppOrder.__name__         , task_model= SuppOrder.__name__        , status=SuppOrder.Status.ERFASST                               , view_url = 'supp_order_alter'        , view_kwargs_id = 'supp_order_id'      , group=Group.objects.get(name=L300))

        #Auftragsreklamationen (Kunde)  
        TaskType.objects.create(id=21   , title = "Bestellreklamation freigeben"                , description ="Bitte geben Sie den Bestellreklamation frei."                                                                                                               , status_model = CustComplaint.__name__     , task_model= CustComplaint.__name__    , status=CustComplaint.Status.ERFASST                           , view_url = 'cust_complaint_alter'    , view_kwargs_id = 'cust_complaint_id'  , group=Group.objects.get(name=K1))
        TaskType.objects.create(id=22   , title = "Bestellreklamation freigeben"                , description ="Bitte geben Sie den Bestellreklamation frei."                                                                                                               , status_model = CustComplaint.__name__     , task_model= CustComplaint.__name__    , status=CustComplaint.Status.ERFASST                           , view_url = 'cust_complaint_alter'    , view_kwargs_id = 'cust_complaint_id'  , group=Group.objects.get(name=K2))
        TaskType.objects.create(id=23   , title = "Bestellreklamation freigeben"                , description ="Bitte geben Sie den Bestellreklamation frei."                                                                                                               , status_model = CustComplaint.__name__     , task_model= CustComplaint.__name__    , status=CustComplaint.Status.ERFASST                           , view_url = 'cust_complaint_alter'    , view_kwargs_id = 'cust_complaint_id'  , group=Group.objects.get(name=K3))
        TaskType.objects.create(id=24   , title = "Bestellreklamation versenden"                , description ="Bitte versenden Sie die Bestellreklamation."                                                                                                                , status_model = CustComplaintDet.__name__  , task_model= CustComplaintDet.__name__ , status=CustComplaintDet.Status.REKLAMATION_FREIGEGEBEN        , view_url = 'cust_complaint_alter'    , view_kwargs_id = 'cust_complaint_id'  , group=Group.objects.get(name=K1)                          , for_all_details=True)
        TaskType.objects.create(id=25   , title = "Bestellreklamation versenden"                , description ="Bitte versenden Sie die Bestellreklamation."                                                                                                                , status_model = CustComplaintDet.__name__  , task_model= CustComplaintDet.__name__ , status=CustComplaintDet.Status.REKLAMATION_FREIGEGEBEN        , view_url = 'cust_complaint_alter'    , view_kwargs_id = 'cust_complaint_id'  , group=Group.objects.get(name=K2)                          , for_all_details=True)
        TaskType.objects.create(id=26   , title = "Bestellreklamation versenden"                , description ="Bitte versenden Sie die Bestellreklamation."                                                                                                                , status_model = CustComplaintDet.__name__  , task_model= CustComplaintDet.__name__ , status=CustComplaintDet.Status.REKLAMATION_FREIGEGEBEN        , view_url = 'cust_complaint_alter'    , view_kwargs_id = 'cust_complaint_id'  , group=Group.objects.get(name=K3)                          , for_all_details=True)
        TaskType.objects.create(id=27   , title = "Bestellreklamation an Produktion senden"     , description ="Bitte versenden Sie die den Hubwagen an die Produktion. Tragen sie die Boxnummer ein."                                                                      , status_model = CustComplaintDet.__name__  , task_model= CustComplaintDet.__name__ , status=CustComplaintDet.Status.REKLAMATION_FREIGEGEBEN        , view_url = 'cust_complaint_alter'    , view_kwargs_id = 'cust_complaint_id'  , group=Group.objects.get(name=KUNDENDIENST)                , for_all_details=True)
        TaskType.objects.create(id=28   , title = "Reklamation bearbeiten"                      , description ="Bitte bearbeiten Sie die Reklamation."                                                                                                                      , status_model = CustComplaintDet.__name__  , task_model= CustComplaintDet.__name__ , status=CustComplaintDet.Status.IN_ANPASSUNG                   , view_url = 'cust_complaint_alter'    , view_kwargs_id = 'cust_complaint_id'  , group=Group.objects.get(name=PRODUKTION)                  , for_all_details=True)
        TaskType.objects.create(id=29   , title = "Boxnummer eintragen"                         , description ="Bitte tragen Sie die Boxnummer in die Reklamation ein und senden Sie die den Hubwagen an den Kundendienst"                                                  , status_model = CustComplaintDet.__name__  , task_model= CustComplaintDet.__name__ , status=CustComplaintDet.Status.ANPASSUNG_ABGESCHLOSSEN        , view_url = 'cust_complaint_alter'    , view_kwargs_id = 'cust_complaint_id'  , group=Group.objects.get(name=PRODUKTION))
        #TaskType.objects.create(id=30, title = "Hubwagen an Kundendienst senden", description ="Bitte senden Sie den Hubwagen an den Kundendienst", group=Group.objects.get(name=PRODUKTION))
        TaskType.objects.create(id=31   , title = "Hubwagen an Kunden senden"                   , description ="Bitte senden Sie den Hubwagen an den Kunden."                                                                                                               , status_model = CustComplaintDet.__name__  , task_model= CustComplaintDet.__name__ , status=CustComplaintDet.Status.BEI_KUNDENDIENST               , view_url = 'cust_complaint_alter'    , view_kwargs_id = 'cust_complaint_id'  , group=Group.objects.get(name=KUNDENDIENST))

        #Bestellreklamation (Lieferant)
        TaskType.objects.create(id=32   , title = "Bestellreklamation freigeben"                , description ="Bitte geben Sie die Bestellreklamation frei."                                                                                                               , status_model = SuppComplaint.__name__     , task_model= SuppComplaint.__name__    , status=SuppComplaint.Status.ERFASST                           , view_url = 'supp_complaint_alter'    , view_kwargs_id = 'supp_complaint_id'  , group=Group.objects.get(name=PRODUKTIONSDIENSTLEISTUNG))
        #TaskType.objects.create(id=33   , title = "Bestellreklamation versenden"                , description ="Bitte tragen Sie die Boxnumemr ein.Bitte schreiben Sie eine Mail an den Lieferanten und versenden die Bestellreklamation"                                   , status_model = SuppComplaint.__name__     , task_model= SuppComplaint.__name__    , status=SuppComplaint.Status.BESTANDSPRUEFUNG_AUSSTEHEND       , view_url = 'supp_complaint_alter'    , view_kwargs_id = 'supp_complaint_id'  , group=Group.objects.get(name=PRODUKTIONSDIENSTLEISTUNG))
        TaskType.objects.create(id=34   , title = "Reklamierte Teile an Produktion senden"      , description ="Bitte senden Sie die reklamierten Teile an das Team Produktion"                                                                                             , status_model = SuppComplaint.__name__     , task_model= SuppComplaint.__name__    , status=-1                                                     , view_url = 'supp_complaint_alter'    , view_kwargs_id = 'supp_complaint_id'  , group=Group.objects.get(name=PRODUKTIONSDIENSTLEISTUNG))
        TaskType.objects.create(id=35   , title = "Fehlteile an PDL senden"                     , description ="Bitte tragen Sie eine Boxnummer ein und senden Sie die Box an die Produktionsdienstleistung"                                                                , status_model = SuppComplaint.__name__     , task_model= SuppComplaint.__name__    , status=SuppComplaint.Status.ERFASST                           , view_url = 'supp_complaint_alter'    , view_kwargs_id = 'supp_complaint_id'  , group=Group.objects.get(name=PRODUKTION))
        #TaskType.objects.create(id=36   , title = "Bestand prüfen"                              , description ="Bitte prüfen Sie den Bestand"                                                                                                                               , status_model = SuppComplaint.__name__     , task_model= SuppComplaint.__name__    , status=SuppComplaint.Status.BESTANDSPRUEFUNG_AUSSTEHEND       , view_url = 'supp_complaint_alter'    , view_kwargs_id = 'supp_complaint_id'  , group=Group.objects.get(name=L300))
        #TaskType.objects.create(id=37   , title = "Neuteile an JOGA senden"                     , description ="Bitte senden Sie die Neuteile an die JOGA. Schreiben Sie eine NAchricht mit der Boxnummer and die JOGA."                                                    , status_model = SuppComplaint.__name__     , task_model= SuppComplaint.__name__    , status=SuppComplaint.Status.BESTANDSPRUEFUNG_AUSSTEHEND       , view_url = 'supp_complaint_alter'    , view_kwargs_id = 'supp_complaint_id'  , group=Group.objects.get(name=L300))
        TaskType.objects.create(id=38   , title = "Reklamation prüfen und freigeben"            , description ="Bitte prüfen Sie die Reklamation und geben Sie diese anschließend frei."                                                                                    , status_model = SuppComplaintDet.__name__  , task_model= SuppComplaintDet.__name__ , status=SuppComplaintDet.Status.REKLAMATION_FREIGEGEBEN        , view_url = 'supp_complaint_alter'    , view_kwargs_id = 'supp_complaint_id'  , group=Group.objects.get(name=PRODUKTIONSDIENSTLEISTUNG)    , for_all_details=True)
        TaskType.objects.create(id=39   , title = "Produtkion aus Lager beliefern"              , description ="Bitte entnehmen Sie die Teile aus dem Lager. Buchen Sie manuell den Warenausgang und schicken Sie die Teile auf direktem Weg zur Produktion."               , status_model = SuppComplaintDet.__name__  , task_model= SuppComplaintDet.__name__ , status=SuppComplaintDet.Status.AUS_LAGER_GELIEFERT            , view_url = 'supp_complaint_alter'    , view_kwargs_id = 'supp_complaint_id'  , group=Group.objects.get(name=PRODUKTIONSDIENSTLEISTUNG))

    def insert_dummy_complaints(apps, schema_editor):

        #L100
        complaint_l100 = SuppOrder(order_no='L100_Teile',ref_no=0,issued_on=0,delivery_date=0,received_on=0,memo='Dies ist für reklamierte Teile des KanBan Systems von L100',status=6,external_system=False,supplier=Supplier.objects.get(name=L100))
        complaint_l100.save()
        complaint_l100_T1 = SuppOrderDet(pos=1,received_on=0,memo='',supp_order=complaint_l100,part=Part.objects.get(part_no='T1'),quantity=0)
        complaint_l100_T1.save()
        complaint_l100_T2 = SuppOrderDet(pos=2,received_on=0,memo='',supp_order=complaint_l100,part=Part.objects.get(part_no='T2'),quantity=0)
        complaint_l100_T2.save()
        complaint_l100_T3 = SuppOrderDet(pos=3,received_on=0,memo='',supp_order=complaint_l100,part=Part.objects.get(part_no='T3'),quantity=0)
        complaint_l100_T3.save()
        complaint_l100_T4 = SuppOrderDet(pos=4,received_on=0,memo='',supp_order=complaint_l100,part=Part.objects.get(part_no='T4'),quantity=0)
        complaint_l100_T4.save()
        complaint_l100_T5 = SuppOrderDet(pos=5,received_on=0,memo='',supp_order=complaint_l100,part=Part.objects.get(part_no='T5'),quantity=0)
        complaint_l100_T5.save()

        #L100 external system
        complaint_l100_external_system = SuppOrder(order_no='L100_Teile',ref_no=0,issued_on=0,delivery_date=0,received_on=0,memo='Dies ist für reklamierte Teile des KanBan Systems von L100',status=6,external_system=True,supplier=Supplier.objects.get(name=L100))
        complaint_l100_external_system.save()
        complaint_l100_external_system_T1 = SuppOrderDet(pos=1,received_on=0,memo='',supp_order=complaint_l100_external_system,part=Part.objects.get(part_no='T1'),quantity=0)
        complaint_l100_external_system_T1.save()
        complaint_l100_external_system_T2 = SuppOrderDet(pos=2,received_on=0,memo='',supp_order=complaint_l100_external_system,part=Part.objects.get(part_no='T2'),quantity=0)
        complaint_l100_external_system_T2.save()
        complaint_l100_external_system_T3 = SuppOrderDet(pos=3,received_on=0,memo='',supp_order=complaint_l100_external_system,part=Part.objects.get(part_no='T3'),quantity=0)
        complaint_l100_external_system_T3.save()
        complaint_l100_external_system_T4 = SuppOrderDet(pos=4,received_on=0,memo='',supp_order=complaint_l100_external_system,part=Part.objects.get(part_no='T4'),quantity=0)
        complaint_l100_external_system_T4.save()
        complaint_l100_external_system_T5 = SuppOrderDet(pos=5,received_on=0,memo='',supp_order=complaint_l100_external_system,part=Part.objects.get(part_no='T5'),quantity=0)
        complaint_l100_external_system_T5.save()

        #L200
        complaint_l200 = SuppOrder(order_no='L200_Teile',ref_no=0,issued_on=0,delivery_date=0,received_on=0,memo='Dies ist für reklamierte Teile des KanBan Systems von L200',status=6,external_system=False,supplier=Supplier.objects.get(name=L200))
        complaint_l200.save()
        complaint_l200_T6 = SuppOrderDet(pos=1,received_on=0,memo='',supp_order=complaint_l200,part=Part.objects.get(part_no='T6'),quantity=0)
        complaint_l200_T6.save()
        complaint_l200_T7 = SuppOrderDet(pos=2,received_on=0,memo='',supp_order=complaint_l200,part=Part.objects.get(part_no='T7'),quantity=0)
        complaint_l200_T7.save()
        complaint_l200_T8 = SuppOrderDet(pos=3,received_on=0,memo='',supp_order=complaint_l200,part=Part.objects.get(part_no='T8'),quantity=0)
        complaint_l200_T8.save()
        complaint_l200_T9 = SuppOrderDet(pos=4,received_on=0,memo='',supp_order=complaint_l200,part=Part.objects.get(part_no='T9'),quantity=0)
        complaint_l200_T9.save()

        #L200 external system
        complaint_l200_external_system = SuppOrder(order_no='L200_Teile',ref_no=0,issued_on=0,delivery_date=0,received_on=0,memo='Dies ist für reklamierte Teile des KanBan Systems von L200',status=6,external_system=True,supplier=Supplier.objects.get(name=L200))
        complaint_l200_external_system.save()
        complaint_l200_external_system_T6 = SuppOrderDet(pos=1,received_on=0,memo='',supp_order=complaint_l200_external_system,part=Part.objects.get(part_no='T6'),quantity=0)
        complaint_l200_external_system_T6.save()
        complaint_l200_external_system_T7 = SuppOrderDet(pos=2,received_on=0,memo='',supp_order=complaint_l200_external_system,part=Part.objects.get(part_no='T7'),quantity=0)
        complaint_l200_external_system_T7.save()
        complaint_l200_external_system_T8 = SuppOrderDet(pos=3,received_on=0,memo='',supp_order=complaint_l200_external_system,part=Part.objects.get(part_no='T8'),quantity=0)
        complaint_l200_external_system_T8.save()
        complaint_l200_external_system_T9 = SuppOrderDet(pos=4,received_on=0,memo='',supp_order=complaint_l200_external_system,part=Part.objects.get(part_no='T9'),quantity=0)
        complaint_l200_external_system_T9.save()

        #L300
        complaint_l300 = SuppOrder(order_no='L300_Teile',ref_no=0,issued_on=0,delivery_date=0,received_on=0,memo='Dies ist für reklamierte Teile des KanBan Systems von L300',status=6,external_system=False,supplier=Supplier.objects.get(name=L300))
        complaint_l300.save()
        complaint_l300_T10 = SuppOrderDet(pos=1,received_on=0,memo='',supp_order=complaint_l300,part=Part.objects.get(part_no='T10'),quantity=0)
        complaint_l300_T10.save()
        complaint_l300_T11 = SuppOrderDet(pos=2,received_on=0,memo='',supp_order=complaint_l300,part=Part.objects.get(part_no='T11'),quantity=0)
        complaint_l300_T11.save()
        complaint_l300_T12 = SuppOrderDet(pos=3,received_on=0,memo='',supp_order=complaint_l300,part=Part.objects.get(part_no='T12'),quantity=0)
        complaint_l300_T12.save()
        complaint_l300_T13 = SuppOrderDet(pos=4,received_on=0,memo='',supp_order=complaint_l300,part=Part.objects.get(part_no='T13'),quantity=0)
        complaint_l300_T13.save()
        complaint_l300_T14 = SuppOrderDet(pos=5,received_on=0,memo='',supp_order=complaint_l300,part=Part.objects.get(part_no='T14'),quantity=0)
        complaint_l300_T14.save()
        complaint_l300_T15 = SuppOrderDet(pos=6,received_on=0,memo='',supp_order=complaint_l300,part=Part.objects.get(part_no='T15'),quantity=0)
        complaint_l300_T15.save()

    
        #L300 external system
        complaint_l300_external_system = SuppOrder(order_no='L300_Teile',ref_no=0,issued_on=0,delivery_date=0,received_on=0,memo='Dies ist für reklamierte Teile des KanBan Systems von L300',status=6,external_system=True,supplier=Supplier.objects.get(name=L300))
        complaint_l300_external_system.save()
        complaint_l300_external_system_T10 = SuppOrderDet(pos=1,received_on=0,memo='',supp_order=complaint_l300_external_system,part=Part.objects.get(part_no='T10'),quantity=0)
        complaint_l300_external_system_T10.save()
        complaint_l300_external_system_T11 = SuppOrderDet(pos=2,received_on=0,memo='',supp_order=complaint_l300_external_system,part=Part.objects.get(part_no='T11'),quantity=0)
        complaint_l300_external_system_T11.save()
        complaint_l300_external_system_T12 = SuppOrderDet(pos=3,received_on=0,memo='',supp_order=complaint_l300_external_system,part=Part.objects.get(part_no='T12'),quantity=0)
        complaint_l300_external_system_T12.save()
        complaint_l300_external_system_T13 = SuppOrderDet(pos=4,received_on=0,memo='',supp_order=complaint_l300_external_system,part=Part.objects.get(part_no='T13'),quantity=0)
        complaint_l300_external_system_T13.save()
        complaint_l300_external_system_T14 = SuppOrderDet(pos=5,received_on=0,memo='',supp_order=complaint_l300_external_system,part=Part.objects.get(part_no='T14'),quantity=0)
        complaint_l300_external_system_T14.save()
        complaint_l300_external_system_T15 = SuppOrderDet(pos=6,received_on=0,memo='',supp_order=complaint_l300_external_system,part=Part.objects.get(part_no='T15'),quantity=0)
        complaint_l300_external_system_T15.save()
        



    dependencies = [
        ('gtapp', '0001_initial'),
        ('gtapp', '0002_insert_usergroups'),
    ]

    operations = [
        migrations.RunPython(insert_customers),
        migrations.RunPython(insert_suppliers),
        migrations.RunPython(insert_parts),
        migrations.RunPython(insert_stocks),
        migrations.RunPython(insert_articles),
        migrations.RunPython(insert_productionsteps),
        migrations.RunPython(insert_bookingcodes),
        migrations.RunPython(insert_tasktypes),
        migrations.RunPython(insert_dummy_complaints),
    ]