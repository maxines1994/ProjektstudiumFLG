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
        c["stock"] = Stock.objects.filter(is_supplier_stock=False)

    if request.user.groups.filter(name=L100).exists():
        c["stock"] = Stock.objects.filter(is_supplier_stock=True, part__supplier_id=1)
    
    if request.user.groups.filter(name=L200).exists():
        c["stock"] = Stock.objects.filter(is_supplier_stock=True, part__supplier_id=2)
    
    if request.user.groups.filter(name=L300).exists():
        c["stock"] = Stock.objects.filter(is_supplier_stock=True, part__supplier_id=3)

    return render(request, "Stock.html", c)

@login_required
def stock_check_view(request, **kwargs):
    c = {}
    # Erst die CustOrderDet holen
    c["custorderdet"] = CustOrderDet.objects.get(pk=kwargs["id"])
    # Dann die Artiparts zu dieser CustOrderDet
    c["artipart"] = c["custorderdet"].get_artiparts(supplier_ids=[3])
    # Bestandsdatensaetze zu diesen Artiparts
    c["stock"] = Stock.objects.filter(is_supplier_stock=False, part_id__in=c["artipart"].values('part_id'))
    # Insgesamt bestellte Menge dieser Teile
    # Betrachte nur SuppOrders von JOGA (external_system=False) und nur welche, die auch verschickt wurden 
    # (status >= BESTELLT und <= GELIEFERT)        
    all_supp_order_dets =   SuppOrderDet.objects.filter(
                                part_id__in=c["stock"].values('part_id'), 
                                supp_order_id__in= SuppOrder.objects.filter(
                                    external_system=False, 
                                    status__gte=SuppOrder.Status.BESTELLT, 
                                    status__lte=SuppOrder.Status.GELIEFERT))
    # Sammle alle Fertigungsauftraege und deren Teile
    all_manu_orders = CustOrderDet.objects.filter(status__gte=CustOrderDet.Status.BESTANDSPRUEFUNG_AUSSTEHEND, status__lte=CustOrderDet.Status.AUFTRAG_FREIGEGEBEN)
    all_manu_orders_parts = Part.objects.filter(supplier_id=3, id__in=ArtiPart.objects.filter(article_id__in=all_manu_orders.values('article_id')))

    # Initialisiere Listen fuer verfuegbaren Bestand, Gesamtbedarf an Teilen und Gesamte Bestellmengen
    stock_available = []
    stock_demand = []
    part_demands = []
    part_ordered_total = []

    # Flag fuer erfolgreiche Bestandspruefung mit True initialisieren
    check_successful = True

    # Durchlaufe alle Bestaende des Kontexts und lege in einer Liste immer den Gesamtbedarf an Teilen dieses Bestandes ab
    s = 0
    for stock in c["stock"]:
        #Verfuegbaren Bestand ermitteln
        temp_available = stock.stock - stock.reserved if stock.stock - stock.reserved >= 0 else 0
        stock_available.append(temp_available)
        # Uebrigen Bedarf ermitteln
        if c["artipart"][s].quantity - temp_available >= 0:
            stock_demand.append(c["artipart"][s].quantity - temp_available)
        else:
            stock_demand.append(0)
        # Bestandspruefung erfolgreich? Hier wird nur auf False gesetzt, falls der Flag True ist.
        # Da eine Liste durchlaufen wird kann jedesmal der Flag wieder auf True gesetzt werden, obwohl
        # ein vorher gepruefter Bestand ihn auf False gesetzt hat. Einmal False, immer False!
        if check_successful:
            check_successful = False if stock_demand[s] - temp_available > 0 else True
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
                # Wenn der naechste Bestand geprueft wird, muss appended werden, ansonsten wird der Bedarf am gleichen Index erhoeht.
                if len(part_ordered_total) <= s:
                    # Wenn Teil bestellt wurde, speichere die Bestellmenge, ansonsten 0
                    if stock.part_id == orderdet.part_id:                 
                        part_ordered_total.append(orderdet.quantity)
                    else:
                        part_ordered_total.append(0)
                else:
                    if stock.part_id == orderdet.part_id:                 
                        part_ordered_total[s] += orderdet.quantity
                    else:
                        part_ordered_total[s] = 0
        s += 1
    # Sicherstellen dass part_ordered_total gefuellt wird, auch wenn es keine Bestellungen gibt.
    if len(part_ordered_total) < s:
        part_ordered_total = [0] * s

    #Fertige Listen in Kontext speichern
    c["stock_available"] = stock_available
    c["stock_demand"] = stock_demand
    c["demand_total"] = part_demands
    c["ordered_total"] = part_ordered_total

    # Boolscher Kontext ob Bestandspruefung erfolgreich
    c["check_successful"] = check_successful

    # Pack Bestande und Artiparts in einen 2-dimensionalen Array
    c["stock_artipart_list"] = zip(c["stock"], c["artipart"])

    # Pack Bestaende, Artiparts, und Gesamtbedarfsmengen in einen Kontext
    # Die Listen existieren zwar lose nebeneinander, vom Index her passen die Daten aber zueinander
    # Wenn alle Listen parallel im Template durchlaufen werden, hat man also die passenden Daten
    c["stock_artipart_stockavailable_stockdemand_orderedtotal_demandtotal"] = zip(c["stock"], c["artipart"], c["stock_available"],c["stock_demand"], c["ordered_total"], c["demand_total"])

    c["STATUS"] = CustOrderDet.Status.__members__

    return render(request, "StockCheck.html", c)
    """
    demand = CustOrderDet.objects.get(pk=kwargs["id"]).part_demand()
    print(demand)
    if Stock.reserve(demand=demand):
        print("ERFOLGREICH")
        CustOrderDet.objects.filter(pk=kwargs["id"]).update(status=CustOrderDet.Status.IN_PRODUKTION)
    else:
        print("FEHLGESCHLAGEN")
    # SETSTATUSTO BESTANDSPRÜFUNG GOOD OR BESTANDSPRÜFUNG BAD
    return HttpResponseRedirect(reverse("manufacturing_list"))
    """

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