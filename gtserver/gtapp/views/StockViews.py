from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from gtapp.models import Stock, StockMovement, Part, BookingCode
from gtapp.constants import *
from gtapp.forms import *
from gtapp.utils import get_context, get_context_back
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, FormView, DetailView

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

def stock_check_view(request, **kwargs):
    c = {}
    c["stock"] = Stock.objects.filter(is_supplier_stock=False, part__supplier_id=3)
    c["custorderdet"] = CustOrderDet.objects.get(pk=kwargs["id"])
    c["demand"] = c["custorderdet"].part_demand()
    c["stock_demand_list"] = zip(c["stock"], c["demand"])

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

class StockmovementView(TemplateView):
    template_name = "StockMovement.html"

    def get_context_data(self, **kwargs):
        my_part_id = self.kwargs['id']
        context = super().get_context_data(**kwargs)
        context = get_context_back(context, "Lagerbewegungen", "")
        context["part"] = Stock.objects.filter(id=my_part_id).first().part
        context["stockmovement"] = StockMovement.objects.filter(stock_id=my_part_id)
        return context

class Stock_alter_view(UpdateView):
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
        print(form.instance.stock)
        myStock = form.save()
        previous = self.request.POST.get('previous','/' )
        print(previous)
        return HttpResponseRedirect(previous)