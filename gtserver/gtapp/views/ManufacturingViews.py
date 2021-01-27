from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from gtapp.models import CustOrderDet, Stock, ArtiPart

def manufacturing_list_view(request):
    c = {}
    c["manufacturing"] = CustOrderDet.objects.filter(cust_order__external_system=False)
    return render(request,"manufacturing.html",c)

def manufacturing_release_view(request,**kwargs):
    c = {}
    return HttpResponseRedirect(reverse(""))

def manufacturing_testing_view(request,**kwargs):
    c = {}
    needs = auto_needs(kwargs["id"])
    if Stock.reserve_test(needs):
        CustOrderDet.objects.filter(pk=kwargs["id"]).update(status='1')
    #SETSTATUSTO BESTANDSPRÜFUNG GOOD OR BESTANDSPRÜFUNG BAD
    return HttpResponseRedirect(reverse("manufacturing_list"))

def manufacturing_supporder_view(request,**kwargs):
    c = {}
    
    return HttpResponseRedirect(reverse(""))

def manufacturing_stock_view(request,**kwargs):
    c = {}
    if request.user.groups.filter(name='JOGA').exists():
        c["stock"] = Stock.objects.filter(is_supplier_stock=False)

    if request.user.groups.filter(name='supplier 100').exists():
        c["stock"] = Stock.objects.filter(is_supplier_stock=True, part__supplier_id=1)
    
    if request.user.groups.filter(name='supplier 200').exists():
        c["stock"] = Stock.objects.filter(is_supplier_stock=True, part__supplier_id=2)
    
    if request.user.groups.filter(name='supplier 300').exists():
        c["stock"] = Stock.objects.filter(is_supplier_stock=True, part__supplier_id=3)

    return render(request,"stock.html",c)
