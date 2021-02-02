from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from gtapp.models import CustOrderDet, Stock, ArtiPart, SuppOrderDet, goods_receipt, CustComplaintDet, SuppComplaintDet, SuppComplaint, SuppOrder
from django.views.generic import CreateView
from gtapp.constants import *
from django.forms import modelformset_factory, ModelChoiceField, NumberInput, Select
from gtapp.forms import formset_goods_cust, formset_goods_cust_c, formset_goods_supp, formset_goods_supp_c


def manufacturing_list_view(request):
    c = {}
    c["manufacturing"] = CustOrderDet.objects.filter(cust_order__external_system=False, status='2')
    return render(request, "manufacturing.html", c)

def manufacturing_release_view(request, **kwargs):
    c = {}
    if CustOrderDet.objects.get(pk=kwargs['id']).status=='0':
        CustOrderDet.objects.filter(pk=kwargs["id"]).update(status='1')
    return HttpResponseRedirect(reverse("cust_order"))

def manufacturing_testing_view(request, **kwargs):
    c = {}
    needs = CustOrderDet.objects.filter(pk=kwargs["id"])[0].auto_needs()
    if Stock.reserve_test(needs):
        print("ERFOLGREICH")
        CustOrderDet.objects.filter(pk=kwargs["id"]).update(status='2')
    else:
        print("FEHLGESCHLAGEN")
    # SETSTATUSTO BESTANDSPRÜFUNG GOOD OR BESTANDSPRÜFUNG BAD
    return HttpResponseRedirect(reverse("manufacturing_list"))

def manufacturing_supporder_view(request, **kwargs):
    c = {}
    
    return HttpResponseRedirect(reverse(""))

def manufacturing_stock_view(request, **kwargs):
    c = {}
    if request.user.groups.filter(name=JOGA).exists():
        c["stock"] = Stock.objects.filter(is_supplier_stock=False)

    if request.user.groups.filter(name=L100).exists():
        c["stock"] = Stock.objects.filter(is_supplier_stock=True, part__supplier_id=1)
    
    if request.user.groups.filter(name=L200).exists():
        c["stock"] = Stock.objects.filter(is_supplier_stock=True, part__supplier_id=2)
    
    if request.user.groups.filter(name=L300).exists():
        c["stock"] = Stock.objects.filter(is_supplier_stock=True, part__supplier_id=3)

    return render(request, "stock.html", c)


def goods_receipt_view(request, **kwargs):
    template = 'goods_receipt.html'
    MyFormSet = None

    # Erstellung der unterschiedlichen Formsets und definierung der Felder + Widgets
    if kwargs['typeofdet'] == 1: # CustOrderDet
        myextra = CustOrderDet.objects.filter(cust_order_id=kwargs['idofdet']).count()
        MyFormSet = modelformset_factory(
            goods_receipt,
            fields=['cust_det', 'quantity', 'delivered', 'trash'],
            extra=myextra,
            widgets={
                'quantity': NumberInput(attrs={'readonly':True}),
                'cust_det': Select(attrs={'disabled':True})
            }
            )
    if kwargs['typeofdet'] == 2: # CustComplaintDet
        myextra = CustComplaintDet.objects.filter(cust_complaint_id=kwargs['idofdet']).count()
        MyFormSet = modelformset_factory(
            goods_receipt,
            fields=['cust_complaint_det', 'quantity', 'delivered', 'trash'],
            extra=myextra,
            widgets={
                'quantity': NumberInput(attrs={'readonly':True}),
                'cust_complaint_det': Select(attrs={'disabled':True})
            }
            )
    if kwargs['typeofdet'] == 3: # SuppOrderDet
        myextra = SuppOrderDet.objects.filter(supp_order_id=kwargs['idofdet']).count()
        MyFormSet = modelformset_factory(
            goods_receipt,
            fields=['supp_det', 'quantity', 'delivered', 'trash'],
            extra=myextra,
            widgets={
                'quantity': NumberInput(attrs={'readonly':True}),
                'supp_det': Select(attrs={'disabled':True})
            }
            )
    if kwargs['typeofdet'] == 4: # SuppComplaintDet
        myextra = SuppComplaintDet.objects.filter(supp_complaint_id=kwargs['idofdet']).count()
        MyFormSet = modelformset_factory(
            goods_receipt,
            fields=['supp_complaint_det', 'quantity', 'delivered', 'trash'],
            extra=myextra,
            widgets={
                'quantity': NumberInput(attrs={'readonly':True}),
                'supp_complaint_det': Select(attrs={'disabled':True})
            }
            )

    # Verarbeitung des Post Requests zur Speicherung der abgeschickten Form
    if request.method == 'POST':
        fs = MyFormSet(request.POST, queryset=goods_receipt.objects.none(), prefix="form1")
        # Form Valid?
        if fs.is_valid():
            fsets = fs.save(commit=False)
            doc = list()

            # Durchgehen aller Forms innerhalb des Formsets
            for fset in fsets:
                fset._creation_user = request.user
                fset.save()
                doc.append(fset.id)
            
            c = None

            # ERSTELLUNG DER REKLAMATIONEN
            if kwargs['typeofdet'] == 1:
                # TBD
                pass
            if kwargs['typeofdet'] == 2:
                # TBD
                pass

            if kwargs['typeofdet'] == 3:
                bo = False
                for i in doc:
                    if goods_receipt.objects.filter(pk=i)[0] != 0:
                        bo = True
                if bo:
                    c = SuppComplaint.objects.create(supp_order_id=kwargs['idofdet'])
                    for i in doc:
                        rd = goods_receipt.objects.get(pk=i)
                        if rd.trash != 0: # POSNR AUTOMATISCH ?!
                            SuppComplaintDet.objects.create(pos=i, supp_complaint_id=c.pk, supp_order_det_id=kwargs["idofdet"], quantity=rd.trash)
            if kwargs['typeofdet'] == 4:
                pass

            return HttpResponseRedirect(reverse("cust_order"))
    else:
        initial = []
        qset = None
        if kwargs['typeofdet'] == 1:
            qset = CustOrderDet.objects.filter(cust_order_id=kwargs['idofdet'])
            for i in qset:
                initial.append({"cust_det":i.pk, "quantity":1})
        if kwargs['typeofdet'] == 2:
            qset = CustComplaintDet.objects.filter(cust_complaint_id=kwargs['idofdet'])
            for i in qset:
                initial.append({"cust_complaint_det":i.pk, "quantity":1})
        if kwargs['typeofdet'] == 3:
            qset = SuppOrderDet.objects.filter(supp_order_id=kwargs['idofdet'])
            for i in qset:
                initial.append({"supp_det":i.pk, "quantity":i.quantity})
        if kwargs['typeofdet'] == 4:
            qset = SuppComplaintDet.objects.filter(supp_complaint_id=kwargs['idofdet'])
            for i in qset:
                initial.append({"supp_complaint_det":i.pk, "quantity":i.quantity})
        formset = MyFormSet(initial=initial, queryset=goods_receipt.objects.none(), prefix='form1')
    return render(request, template, {'formset':formset})

