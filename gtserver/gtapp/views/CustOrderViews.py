from gtapp.utils import get_context
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from gtapp.forms import Cust_order_form

def cust_order_list_view(request):
    c = get_context("Kundenaufträge","Aufträge")
    return render(request, "tasks_list.html", c)

def cust_order_create_view(request):
    c = get_context("Kundenauftrag erstellen","Aufträge")

    print(request)

    if request.method == "GET":
        c["form"] = Cust_order_form()
        return render(request, "CustOrderForm.html", c)
    
    if request.method == "POST":
        form = Cust_order_form(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/CustOrder_list/")

def cust_order_alter_view(request):
    c = get_context("Kundenauftrag ändern","Aufträge")

    print(request)

    if request.method == "GET":
        c["form"] = Cust_order_form()
        return render(request, "CustOrderForm.html", c)
    
    if request.method == "POST":
        form = Cust_order_form(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/CustOrder_list/")

