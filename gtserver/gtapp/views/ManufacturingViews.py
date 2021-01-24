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
    erg = Stock.reserve_test(needs)
    #SETSTATUSTO BESTANDSPRÜFUNG GOOD OR BESTANDSPRÜFUNG BAD
    return HttpResponseRedirect(reverse("manufacturing_list"))

def manufacturing_supporder_view(request,**kwargs):
    c = {}
    
    return HttpResponseRedirect(reverse(""))

def auto_needs(cust_order_det):
    cod = CustOrderDet.objects.get(pk=cust_order_det)
    needs = list()
    atpt = ArtiPart.objects.filter(article_id=cod.article.id, part__supplier_id=3)
    for p in atpt:
        needs.append((p.part, p.quantity))
    return needs

