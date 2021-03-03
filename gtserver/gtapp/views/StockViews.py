from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.db.models import Count, Sum
from gtapp.models import *
from gtapp.constants import *
from gtapp.forms import *
from gtapp.utils import get_context, get_context_back
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

@login_required
def stock_view(request, **kwargs):
    c = {}
    if request.user.groups.filter(name=JOGA).exists():
        c["stock"] = Stock.objects.filter(is_supplier_stock=False, part__supplier_id=3)

    if request.user.groups.filter(name=L100).exists():
        c["stock"] = Stock.objects.filter(is_supplier_stock=True, part__supplier_id=1)
    
    if request.user.groups.filter(name=L200).exists():
        c["stock"] = Stock.objects.filter(is_supplier_stock=True, part__supplier_id=2)
    
    if request.user.groups.filter(name=L300).exists():
        c["stock"] = Stock.objects.filter(is_supplier_stock=True, part__supplier_id=3)

    return render(request, "Stock.html", c)

@login_required
def stock_check_view(request, **kwargs):

    is_supplier = request.user.groups.filter(name=LIEFERANTEN).exists()
    is_complaint = 'complaint' in request.META['HTTP_REFERER'] or request.POST.get('is_complaint')
    c = {}
    c['is_complaint'] = is_complaint
    # Erst die CustOrderDet holen
    if is_supplier:
        if is_complaint:
            # Liste nur die Complaints die nachgeliefert werden sollen
            my_suppcomplaint_dets = SuppComplaintDet.objects.filter(supp_complaint_id=kwargs["id"]).exclude(redelivery=False)
            my_supporder_dets = SuppOrderDet.objects.filter(id__in=my_suppcomplaint_dets.values('supp_order_det_id'))
        else:
            my_supporder_dets = SuppOrderDet.objects.filter(supp_order_id=kwargs["id"])

        my_supporder_parts = Part.objects.filter(id__in=my_supporder_dets.values("part_id"))
        # Bestandsdatensaetze zu den Teilen
        c["stock"] = Stock.objects.filter(is_supplier_stock=is_supplier, part__in=my_supporder_parts)
        c["supporderdet"] = my_supporder_dets
        c["part"] = SuppOrderDet.objects.filter(supp_order_id=kwargs["id"]).values('part_id')
    else:
        c["custorderdet"] = CustOrderDet.objects.get(pk=kwargs["id"])
        # Dann die Artiparts zu dieser CustOrderDet
        c["artipart"] = c["custorderdet"].get_artiparts(supplier_ids=[3])
        # Bestandsdatensaetze zu diesen Artiparts
        c["stock"] = Stock.objects.filter(is_supplier_stock=is_supplier, part_id__in=c["artipart"].values('part_id'))
    # Insgesamt bestellte Menge dieser Teile
    # Betrachte nur SuppOrders von JOGA (external_system=False) und nur welche, die auch verschickt wurden 
    # (status >= BESTELLT und <= GELIEFERT)       
    status_min = SuppOrder.Status.ERFASST if is_supplier else SuppOrder.Status.BESTELLT
    status_max = SuppOrder.Status.TEILGELIEFERT if is_supplier else SuppOrder.Status.TEILGELIEFERT

    all_supp_order_dets =   SuppOrderDet.objects.filter(
                                part_id__in=c["stock"].values('part_id'), 
                                supp_order_id__in= SuppOrder.objects.filter(
                                    external_system=is_supplier, 
                                    status__gte=status_min, 
                                    status__lte=status_max))
# Sammle alle Fertigungsauftraege und deren Teile
    all_manu_orders = CustOrderDet.objects.filter(status__gte=CustOrderDet.Status.BESTANDSPRUEFUNG_AUSSTEHEND, status__lte=CustOrderDet.Status.AUFTRAG_FREIGEGEBEN)
    all_manu_orders_parts = Part.objects.filter(supplier_id=3, id__in=ArtiPart.objects.filter(article_id__in=all_manu_orders.values('article_id')))

    # Initialisiere Listen fuer verfuegbaren Bestand, Gesamtbedarf an Teilen und Gesamte Bestellmengen
    stock_available = []
    stock_demand = []
    part_demands = []
    part_ordered_total = []
    part_order_suggestions = []

    # Flag fuer erfolgreiche Bestandspruefung mit True initialisieren
    check_successful = True

    if is_supplier:
        for s, stock in enumerate(c["stock"]):
            #Verfuegbaren Bestand ermitteln
            temp_available = stock.stock - stock.reserved if stock.stock - stock.reserved >= 0 else 0
            stock_available.append(temp_available)
            # Uebrigen Bedarf ermitteln
            if my_supporder_dets[s].quantity - temp_available >= 0:
                stock_demand.append(my_supporder_dets[s].quantity - temp_available)
            else:
                stock_demand.append(0)

    else:
        # Durchlaufe alle Bestaende des Kontexts und lege in einer Liste immer den Gesamtbedarf an Teilen dieses Bestandes ab
        for s, stock in enumerate(c["stock"]):
            #Verfuegbaren Bestand ermitteln
            temp_available = stock.stock - stock.reserved if stock.stock - stock.reserved >= 0 else 0
            stock_available.append(temp_available)
            # Uebrigen Bedarf ermitteln
            if c["artipart"][s].quantity - temp_available >= 0:
                stock_demand.append(c["artipart"][s].quantity - temp_available)
            else:
                stock_demand.append(0)
            # Bestandspruefung erfolgreich? Hier wird nur auf False gesetzt, falls der Flag True ist.
            # Beim Durchlaufen der Liste kann der Flag nicht wieder auf True gesetzt werden, wenn
            # ein vorher gepruefter Bestand ihn einmal auf False gesetzt hat. Einmal False, immer False!
            if check_successful:
                check_successful = False if temp_available - stock_demand[s]  <= 0 else True
            # Durchlaufe alle relevanten Fertigungsauftraege
            for order in all_manu_orders:
                # Pruefe nur die Artiparts, die fuer den Artikel des Auftrages existieren.
                # Sonst knallts naemlich spaeter beim ArtiPart.objects.get
                if ArtiPart.objects.filter(article_id=order.article_id, part_id=stock.part_id).exists():
                    # Wenn der naechste Bestand geprueft wird, muss appended werden, ansonsten wird der Bedarf am gleichen Index erhoeht.
                    if len(part_demands) <= s:
                        part_demands.append(ArtiPart.objects.get(article_id=order.article_id, part_id=stock.part_id).quantity)
                    else:
                        part_demands[s] += ArtiPart.objects.get(article_id=order.article_id, part_id=stock.part_id).quantity
            # Durchlaufe alle relevanten Bestellungen
            for orderdet in all_supp_order_dets:
                    # Immer wenn der naechste Bestand geprueft wird, ist die Liste der insgesamt bestellten Teile noch 
                    # kuerzer, als der Iterator. Wenn der naechste Bestand geprueft wird, muss also appended werden, 
                    # ansonsten wird der Bedarf am gleichen Index erhoeht.
                    if len(part_ordered_total) <= s:
                        # Wenn das Teil in der aktuell geprueften Bestellung vorhanden ist, speichere die Bestellmenge, ansonsten 0
                        if stock.part_id == orderdet.part_id:                 
                            part_ordered_total.append(orderdet.quantity)
                        else:
                            part_ordered_total.append(0)
                    else:
                        if stock.part_id == orderdet.part_id:                 
                            part_ordered_total[s] += orderdet.quantity

        # Sicherstellen dass part_ordered_total mit nullen gefuellt wird, wenn es keine Bestellungen gibt.
        if len(part_ordered_total) == 0:
            part_ordered_total = [0] * s
    
        for p, parts in enumerate(c["stock"]):
            my_part_suggestion = part_demands[p] - part_ordered_total[p] - stock_available[p]
            if my_part_suggestion >= 0:
                part_order_suggestions.append(my_part_suggestion)
            else:
                part_order_suggestions.append(0)
        

    #Fertige Listen in Kontext speichern
    c["stock_available"] = stock_available
    c["stock_demand"] = stock_demand
    c["demand_total"] = part_demands
    c["ordered_total"] = part_ordered_total
    c["order_suggestions"] = part_order_suggestions
    # Boolscher Kontext ob Bestandspruefung erfolgreich
    c["check_successful"] = check_successful

    if is_supplier:
        if is_complaint:
            # Bei Reklamationen Kontext auf Reklamationspositionen aendern, damit die Quantity der Reklamation
            # und nicht der zugrundeliegenden Bestellung aufgelistet wird
            c["supporderdet"] = my_suppcomplaint_dets
        c["stock_supporderdet_stockavailable"] = zip(c["stock"], c["supporderdet"], c["stock_available"])

    else: 
        # Pack Bestaende, Artiparts, und Gesamtbedarfsmengen in einen Kontext
        # Die Listen existieren zwar lose nebeneinander, vom Index her passen die Daten aber zueinander
        # Wenn alle Listen parallel im Template durchlaufen werden, hat man also die passenden Daten
        c["stock_artipart_stockavailable_stockdemand_orderedtotal_demandtotal_suggestion"] = zip(c["stock"], c["artipart"], c["stock_available"],c["stock_demand"], c["ordered_total"], c["demand_total"],c["order_suggestions"])


    c["STATUS"] = CustOrderDet.Status.__members__ if not is_supplier else SuppOrder.Status.__members__

    # Hier gehts um Automatische Bestellungen und Abschluss der Bestandspruefung
    if request.method == 'POST':
        part_id_list = []
        order_quantity_list = []
        status_task_kwargs = {}
        i = 1
        # Im Template werden die Zeilen gezaehlt. Laufe jede Zeile durch und speichere die dazugehoerige
        # part_id und order_quantity in Listen
        while i <= int(request.POST.get("rows")):
            part_id_list.append(request.POST.get('part_id' + str(i)))
            if not check_successful:
                # Nur Listen fuellen mit Teilen die eine Bestellmenge > 0 haben
                if int(request.POST.get('order_quantity' + str(i))) > 0:
                    order_quantity_list.append(request.POST.get('order_quantity' + str(i)))
            i += 1

        # Bei automatischen Bestellungen:
        if not check_successful:    
            my_new_supporder_id = SuppOrderDet.auto_order(part_id_list, order_quantity_list)
            status_task_kwargs['id'] = my_new_supporder_id
            status_task_kwargs['task_type'] = 15 #Bestellung freigeben
        
        # Bei Abschluss der Bestandspruefung werden die Mengen reserviert und ein neuer status_task gesetzt
        if check_successful:
            # Teile der Liste durchlaufen und jeweils die Mengen reservieren
            for part_id in part_id_list:
                my_part = Part.objects.get(id=part_id)
                my_stock = Stock.objects.get(part_id=part_id, is_supplier_stock=is_supplier)
                if is_supplier:
                    my_supporder_det = my_supporder_dets.filter(part=my_part).first()
                    if is_complaint:
                        my_suppcomplaint_det = my_suppcomplaint_dets.filter(supp_order_det_id=my_supporder_det).first()
                        # Keine Menge reservieren, wenn Nachlieferung nicht notwendig
                        my_quantity = my_suppcomplaint_det.quantity if my_suppcomplaint_det.redelivery else 0
                    else:
                        my_quantity = my_supporder_det.quantity
                else:
                    my_quantity = my_part.install_quantity
                my_stock.reserve(quantity=my_quantity)
            # fuelle kwargs fuer Weiterleitung an set_status_task
            status_task_kwargs['id'] = kwargs['id']

            if is_supplier:
                #Teilelieferung an JOGA
                if is_complaint:
                    if request.user.groups.filter(name=L100).exists():
                        my_task_type = 44
                    elif request.user.groups.filter(name=L200).exists():
                        my_task_type = 45
                    elif request.user.groups.filter(name=L300).exists():
                        my_task_type = 46
                else:
                    my_task_type = 10
            else:
                my_task_type = 5 #Teilelieferung an Produktion

            status_task_kwargs['task_type'] = my_task_type 

        return HttpResponseRedirect(reverse("set_status_task", kwargs=status_task_kwargs))

    return render(request, "StockCheck.html", c)

@login_required
def stock_check_complete(request, **kwargs):
    part_ids = []
    rows = int(request.POST.get('rows'))
    # Durchlaufe alle Zeilen der Bestandspruefungsliste und speichere die Teile-IDs
    i = 0
    while i <= int(request.POST.get('rows')):
        part_ids.append(request.POST.get('part_id' + str(i)))
        i += 1
    
    # Durchlaufe die Liste der Teile-IDs und reserviere die Bestaende entsprechend der part.install_quantity
    for part_id in part_ids:
        my_part = Part.objects.get(id=part_ids[part_id])
        my_stock = Stock.objects.get(part_id=my_part_id, is_supplier_stock=False)
        my_stock.reserve(quantity=my_part.install_quantity)

    return HttpResponseRedirect(reverse("set_status_task", kwargs={id: kwargs['id'], todo_type: kwargs['task_type']}))


class StockmovementView(LoginRequiredMixin, TemplateView):
    template_name = "StockMovement.html"

    def get_context_data(self, **kwargs):
        my_part_id = self.kwargs['id']
        context = super().get_context_data(**kwargs)
        context = get_context_back(context, "Lagerbewegungen", "")
        context["part"] = Stock.objects.filter(id=my_part_id).first().part
        context["stockmovement"] = StockMovement.objects.filter(stock_id=my_part_id)
        return context

class Stock_alter_view(LoginRequiredMixin, UpdateView):
    template_name = "StockForm.html"
    form_class = Stock_form 

    # Context zum Templating hinzufügen 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock'] = self.get_object()
        return context

    # Objekt für Alter view getten
    def get_object(self, queryset=None):
        obj = Stock.objects.get(id=self.kwargs['id'])
        return obj
      
    def form_valid(self, form):
        myStock = Stock.objects.get(id=self.kwargs['id'])
        currentStock = myStock.stock
        myStock.change(booking_quantity=form.instance.stock - currentStock, booking_code=BookingCode.objects.get(code=BUCHUNG_KORREKTURBUCHUNG).code)
        myStock = form.save()
        previous = self.request.POST.get('previous','/' )
        return HttpResponseRedirect(previous)