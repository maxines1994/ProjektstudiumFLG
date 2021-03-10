from . import *
from django.shortcuts import render

def dashboard(request):
    ##Queries and data
    all_cust_orders = CustOrder.objects.all().exclude(external_system=True)
    all_cust_order_dets = CustOrderDet.objects.all()

    all_cust_complaints = CustComplaint.objects.all().exclude(external_system=True)
    all_cust_complaint_dets = CustComplaintDet.objects.all()

    all_supp_orders = SuppOrder.objects.all().exclude(external_system=True).exclude(id__in=[1,2,3,4,5,6])

    all_supp_complaints = SuppComplaint.objects.all().exclude(external_system=True)

    all_messages = Message.objects.all()

    current_gameday = Timers.get_current_day()

    ##001 Anzahl Hubwagen nach Status 
    labels_001 = ['Erfasst','Freigegeben','Teile reserviert','Komissioniert','In Produktion','Produktion abgeschlossen','An Kundendienst versandt','Bereit zum Versand an Kunden','Teilgeliefert','Geliefert','Abgenommen','Storniert']
    data_001 = []

    data_001.append(all_cust_order_dets.filter(status=CustOrderDet.Status.ERFASST).count()) ## Erfasst
    data_001.append(all_cust_order_dets.filter(status=CustOrderDet.Status.BESTANDSPRUEFUNG_AUSSTEHEND).count()) ## Freigegeben
    data_001.append(all_cust_order_dets.filter(status=CustOrderDet.Status.BESTANDSPRUEFUNG_ABGESCHLOSSEN).count()) ## Teile reserviert
    data_001.append(all_cust_order_dets.filter(status=CustOrderDet.Status.AUFTRAG_FREIGEGEBEN).count()) ## Komissioniert
    data_001.append(all_cust_order_dets.filter(status=CustOrderDet.Status.IN_PRODUKTION).count()) ## In Produktion
    data_001.append(all_cust_order_dets.filter(status=CustOrderDet.Status.LIEFERUNG_AN_KD_AUSSTEHEND).count()) ## Produktion Abgeschlossen
    data_001.append(all_cust_order_dets.filter(status=CustOrderDet.Status.VERSANDT_AN_KD).count()) ## An Kundendienst versandt
    data_001.append(all_cust_order_dets.filter(status=CustOrderDet.Status.LIEFERUNG_AN_K_AUSSTEHEND).count()) ## Bereit zum Versand an Kunden
    data_001.append(all_cust_order_dets.filter(status=CustOrderDet.Status.VERSANDT_AN_K).count()) ## Teilgeliefert
    data_001.append(all_cust_order_dets.filter(status=CustOrderDet.Status.GELIEFERT).count()) ## Geliefert
    data_001.append(all_cust_order_dets.filter(status=CustOrderDet.Status.ABGENOMMEN).count()) ## Abgenommen
    data_001.append(all_cust_order_dets.filter(status=CustOrderDet.Status.STORNIERT).count()) ## Abgenommen
    

    #002 Auftragsreklamationen nach Status
    labels_002 = ['Erfasst', 'Freigegeben', 'Versand an Produktion', 'In Anpassung','Anpassung abgeschlossen','Versand an Kundendienst', 'Bereit zum Versand an Kunde','Geliefert','Abgeschlossen']
    data_002 = []

    data_002.append(all_cust_complaint_dets.filter(status=CustComplaintDet.Status.ERFASST).count()) ## Erfasst
    data_002.append(all_cust_complaint_dets.filter(status=CustComplaintDet.Status.REKLAMATION_FREIGEGEBEN).count()) ## Freigegeben
    data_002.append(all_cust_complaint_dets.filter(status=CustComplaintDet.Status.VERSAND_AN_PRODUKTION).count()) ## Versand an Produktion
    data_002.append(all_cust_complaint_dets.filter(status=CustComplaintDet.Status.IN_ANPASSUNG).count()) ## In Anpassung
    data_002.append(all_cust_complaint_dets.filter(status=CustComplaintDet.Status.ANPASSUNG_ABGESCHLOSSEN).count()) ## Anpassung abgeschlossen
    data_002.append(all_cust_complaint_dets.filter(status=CustComplaintDet.Status.VERSAND_AN_KUNDENDIENST).count()) ## Versand an Kundendienst
    data_002.append(all_cust_complaint_dets.filter(status=CustComplaintDet.Status.BEI_KUNDENDIENST).count()) ## Bereit zum Versand an Kundendienst
    data_002.append(all_cust_complaint_dets.filter(status=CustComplaintDet.Status.GELIEFERT).count()) ## Geliefert
    data_002.append(all_cust_complaint_dets.filter(status=CustComplaintDet.Status.ABGESCHLOSSEN).count()) ## Abgeschlossen


    ##003 Bestellungen nach Status
    labels_003 = ['Erfasst','Bestellt','Teilgeliefert','Geliefert','Storniert']
    data_003 = []

    data_003.append(all_supp_orders.filter(status=SuppOrder.Status.ERFASST).count()) ## Erfasst
    data_003.append(all_supp_orders.filter(status=SuppOrder.Status.BESTELLT).count()) ## Bestellt
    data_003.append(all_supp_orders.filter(status=SuppOrder.Status.TEILGELIEFERT).count()) ## Teilgeliefert
    data_003.append(all_supp_orders.filter(status=SuppOrder.Status.GELIEFERT).count()) ## Geliefert
    data_003.append(all_supp_orders.filter(status=SuppOrder.Status.STORNIERT).count()) ## Storniert


    ##004 Bestellreklamationen nach Status
    labels_004 = ['Erfasst','Versandt an PDL','In Bearbeitung','Freigegeben','Positionsbearbeitung abgeschlossen','Versandt an Lieferant','Ersatzteile geliefert','Versandt an Produktion','Abgeschlossen']
    data_004 = []

    data_004.append(all_supp_complaints.filter(status=SuppComplaint.Status.ERFASST).count()) ## Erfasst
    data_004.append(all_supp_complaints.filter(status=SuppComplaint.Status.VERSAND_AN_PDL).count()) ## Versandt an PDL
    data_004.append(all_supp_complaints.filter(status=SuppComplaint.Status.IN_BEARBEITUNG).count()) ## In Bearbeitung
    data_004.append(all_supp_complaints.filter(status=SuppComplaint.Status.REKLAMATION_FREIGEGEBEN).count()) ## Freigegeben
    data_004.append(all_supp_complaints.filter(status=SuppComplaint.Status.POSITIONSBEARBEITUNG_FERTIG).count()) ## Positionsbearbeitung abegschlossen
    data_004.append(all_supp_complaints.filter(status=SuppComplaint.Status.VERSAND_AN_LIEFERANT).count()) ## Versandt an Lieferant
    data_004.append(all_supp_complaints.filter(status=SuppComplaint.Status.GELIEFERT).count()) ## Ersatzteile geliefert
    data_004.append(all_supp_complaints.filter(status=SuppComplaint.Status.VERSAND_AN_PRODUKTION).count()) ## Versandt an Produktion
    data_004.append(all_supp_complaints.filter(status=SuppComplaint.Status.ABGESCHLOSSEN).count()) ## Abgeschlossen


    ##005 Übersicht Aufträge vs Reklamationen nach Kunden
    labels_005 = ['Kunde 1','Kunde 2','Kunde 3']
    ## Auftragsdaten
    data_005_1 = []
    ## Reklamationsdaten
    data_005_2 = []

    data_005_1.append(all_cust_order_dets.filter(cust_order__in=all_cust_orders.filter(customer=1)).count())
    data_005_1.append(all_cust_order_dets.filter(cust_order__in=all_cust_orders.filter(customer=2)).count())
    data_005_1.append(all_cust_order_dets.filter(cust_order__in=all_cust_orders.filter(customer=3)).count())

    data_005_2.append(all_cust_complaint_dets.filter(cust_order_det__in=all_cust_order_dets.filter(cust_order__in=all_cust_orders.filter(customer=1))).count())
    data_005_2.append(all_cust_complaint_dets.filter(cust_order_det__in=all_cust_order_dets.filter(cust_order__in=all_cust_orders.filter(customer=2))).count())
    data_005_2.append(all_cust_complaint_dets.filter(cust_order_det__in=all_cust_order_dets.filter(cust_order__in=all_cust_orders.filter(customer=3))).count())


    ##006 Übersicht Aufträge vs Reklamationen nach Kunden
    labels_006 = ['Lieferant 1','Lieferant 2','Lieferant 3']
    ## Auftragsdaten
    data_006_1 = []
    ## Reklamationsdaten
    data_006_2 = []

    data_006_1.append(all_supp_orders.filter(supplier=1).count())
    data_006_1.append(all_supp_orders.filter(supplier=2).count())
    data_006_1.append(all_supp_orders.filter(supplier=3).count())

    data_006_2.append(all_supp_complaints.filter(supp_order__in=all_supp_orders.filter(supplier=1)).count())
    data_006_2.append(all_supp_complaints.filter(supp_order__in=all_supp_orders.filter(supplier=2)).count())
    data_006_2.append(all_supp_complaints.filter(supp_order__in=all_supp_orders.filter(supplier=3)).count())


    #007 Spieltaganalyse
    labels_007 = []

    ## Aufträge
    data_007_1 = []

    ## Auftragsreklamationen
    data_007_2 = []

    ## Bestellungen
    data_007_3 = []

    ## Bestellreklamationen
    data_007_4 = []

    ## Nachrichten
    data_007_5 = []

    for day in range(1,current_gameday+1):
        labels_007.append('Tag '+str(day))

        data_007_1.append(all_cust_order_dets.filter(_creation_gameday=day).count())
        data_007_2.append(all_cust_complaint_dets.filter(_creation_gameday=day).count())
        data_007_3.append(all_supp_orders.filter(_creation_gameday=day).count())
        data_007_4.append(all_supp_complaints.filter(_creation_gameday=day).count())
        data_007_5.append(all_messages.filter(_creation_gameday=day).count())

    #008 Übersicht Aufträge Lieferverzug
    data_008 = []
    for cust_order in all_cust_orders.exclude(status=CustOrder.Status.ABGENOMMEN).exclude(status=CustOrder.Status.STORNIERT):
        days_until_delivery = cust_order.delivery_date - current_gameday
        if days_until_delivery >= 1 and days_until_delivery <= 3:
            data_set_color = '#f58a42' ##Orange
            data_set_font_weight = 'bold'
        elif days_until_delivery <= 0:
            data_set_color = '#e60000' ##Red
            data_set_font_weight = 'bolder'
        else:
            data_set_color = '#000000' ##Schwarz
            data_set_font_weight = 'normal'

        data_008.append({'cust_order':cust_order,'days_until_delivery':days_until_delivery,'data_set_color':data_set_color,'data_set_font_weight':data_set_font_weight})

    #data_008.sort(key='days_until_delivery')
    data_008 = sorted(data_008, key=lambda k: k['days_until_delivery']) 


    return render(request, 'dashboard.html', {
        'labels_001': labels_001,
        'data_001': data_001,

        'labels_002': labels_002,
        'data_002': data_002,  

        'labels_003': labels_003,
        'data_003': data_003,

        'labels_004': labels_004,
        'data_004': data_004,

        'labels_005': labels_005,
        'data_005_1': data_005_1,
        'data_005_2': data_005_2,

        'labels_006': labels_006,
        'data_006_1': data_006_1,
        'data_006_2': data_006_2,

        'labels_007': labels_007,
        'data_007_1': data_007_1,
        'data_007_2': data_007_2,
        'data_007_3': data_007_3,
        'data_007_4': data_007_4,
        'data_007_5': data_007_5,

        'data_008': data_008,
    })